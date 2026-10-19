"""SQLite-backed idempotent observation intake for the Phase 1 prototype.

This is a local prototype store, not a network-facing ingestion API. Production
deployment still requires authenticated transport, authorization, rate/size
limits, migrations, backup/restore and security review.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .contract import validate_observation


class ObservationStore:
    def __init__(self, database_path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                record_id TEXT PRIMARY KEY,
                payload_hash TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                environment TEXT NOT NULL,
                received_at TEXT NOT NULL
            )
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_conflicts (
                conflict_id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT NOT NULL,
                existing_hash TEXT NOT NULL,
                incoming_hash TEXT NOT NULL,
                incoming_payload_json TEXT NOT NULL,
                detected_at TEXT NOT NULL
            )
        """)
        self.connection.commit()

    @staticmethod
    def _canonical_payload(record: dict[str, Any]) -> tuple[str, str]:
        payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return payload, digest

    def ingest(self, record: dict[str, Any]) -> str:
        """Return INSERTED, DUPLICATE or CONFLICT; invalid records raise ContractError."""
        validate_observation(record)
        payload, digest = self._canonical_payload(record)
        record_id = record["record_id"]
        existing = self.connection.execute(
            "SELECT payload_hash FROM observations WHERE record_id = ?", (record_id,)
        ).fetchone()
        if existing is None:
            self.connection.execute(
                "INSERT INTO observations(record_id,payload_hash,payload_json,environment,received_at) VALUES(?,?,?,?,?)",
                (record_id, digest, payload, record["environment"], datetime.now(timezone.utc).isoformat()),
            )
            self.connection.commit()
            return "INSERTED"
        if existing["payload_hash"] == digest:
            return "DUPLICATE"
        self.connection.execute(
            "INSERT INTO ingestion_conflicts(record_id,existing_hash,incoming_hash,incoming_payload_json,detected_at) VALUES(?,?,?,?,?)",
            (record_id, existing["payload_hash"], digest, payload, datetime.now(timezone.utc).isoformat()),
        )
        self.connection.commit()
        return "CONFLICT"

    def get(self, record_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT payload_json FROM observations WHERE record_id = ?", (record_id,)
        ).fetchone()
        return json.loads(row["payload_json"]) if row else None

    def conflict_count(self, record_id: str | None = None) -> int:
        if record_id is None:
            row = self.connection.execute("SELECT COUNT(*) AS n FROM ingestion_conflicts").fetchone()
        else:
            row = self.connection.execute(
                "SELECT COUNT(*) AS n FROM ingestion_conflicts WHERE record_id = ?", (record_id,)
            ).fetchone()
        return int(row["n"])

    def close(self) -> None:
        self.connection.close()
