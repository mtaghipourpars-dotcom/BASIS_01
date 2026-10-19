"""Dependency-free validation for canonical Phase 1 observations.

This module validates envelope invariants only. Source-specific semantics and
JSON Schema validation remain separate acceptance gates.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

ENVIRONMENTS = {"DEMO", "TEST", "LIVE"}
RECORD_TYPES = {"metric", "event"}
QUALITY_STATUSES = {"VALID", "INVALID", "PARTIAL", "UNAVAILABLE"}
FRESHNESS = {"FRESH", "STALE", "UNKNOWN"}
COMPUTED_STATUSES = {"HEALTHY", "ATTENTION", "CRITICAL", "UNKNOWN", "STALE", "NOT_SUPPORTED"}


class ContractError(ValueError):
    """Raised when a record violates the canonical envelope contract."""


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{field} must be a non-empty ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_observation(record: dict[str, Any]) -> None:
    """Validate a metric/event envelope; raises ContractError on first failure."""
    if not isinstance(record, dict):
        raise ContractError("record must be an object")
    required = {"schema_version", "record_type", "record_id", "environment", "target", "source", "quality", "evidence_ref"}
    missing = sorted(required - record.keys())
    if missing:
        raise ContractError(f"missing required fields: {', '.join(missing)}")
    if record["schema_version"] != "1.0":
        raise ContractError("unsupported schema_version")
    if record["record_type"] not in RECORD_TYPES:
        raise ContractError("record_type must be metric or event")
    if not isinstance(record["record_id"], str) or not record["record_id"].strip():
        raise ContractError("record_id must be a non-empty string")
    if record["environment"] not in ENVIRONMENTS:
        raise ContractError("environment must be DEMO, TEST or LIVE")
    if not isinstance(record["target"], dict) or not record["target"].get("system_id"):
        raise ContractError("target.system_id is required")
    if not isinstance(record["source"], dict) or not record["source"].get("adapter_id"):
        raise ContractError("source.adapter_id is required")
    if not isinstance(record["quality"], dict):
        raise ContractError("quality must be an object")
    if record["quality"].get("status") not in QUALITY_STATUSES:
        raise ContractError("invalid quality.status")
    if record["quality"].get("freshness") not in FRESHNESS:
        raise ContractError("invalid quality.freshness")
    if not isinstance(record["evidence_ref"], str) or not record["evidence_ref"].strip():
        raise ContractError("evidence_ref is required")

    _parse_timestamp(record.get("received_at"), "received_at")
    if record["record_type"] == "metric":
        metric = record.get("metric")
        if not isinstance(metric, dict):
            raise ContractError("metric record requires metric object")
        if not metric.get("id") or not metric.get("unit"):
            raise ContractError("metric.id and metric.unit are required")
        value = metric.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ContractError("metric.value must be numeric; missing data is not zero")
        _parse_timestamp(record.get("observed_at"), "observed_at")
    else:
        event = record.get("event")
        if not isinstance(event, dict) or not event.get("event_type") or not event.get("status"):
            raise ContractError("event record requires event_type and status")
        first = _parse_timestamp(record.get("first_observed_at"), "first_observed_at")
        last = _parse_timestamp(record.get("last_observed_at"), "last_observed_at")
        if first > last:
            raise ContractError("first_observed_at must not be after last_observed_at")


def freshness_state(last_success_at: str | None, now: datetime, stale_after_seconds: int) -> str:
    """Return UNKNOWN for absent/invalid evidence, otherwise FRESH or STALE."""
    if stale_after_seconds < 0:
        raise ValueError("stale_after_seconds must be non-negative")
    if not last_success_at:
        return "UNKNOWN"
    try:
        observed = _parse_timestamp(last_success_at, "last_success_at")
    except ContractError:
        return "UNKNOWN"
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    age = (now.astimezone(timezone.utc) - observed).total_seconds()
    if age < 0:
        return "UNKNOWN"
    return "STALE" if age > stale_after_seconds else "FRESH"
