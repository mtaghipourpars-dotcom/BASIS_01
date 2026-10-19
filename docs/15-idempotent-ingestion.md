# 15 — Idempotent Ingestion Prototype

**Status:** local SQLite prototype; not a production API.

## Behavior
- Validates records against the common envelope validator before persistence.
- Uses deterministic canonical JSON and SHA-256 payload hashes.
- First valid record ID is stored as `INSERTED`.
- Same ID and same payload returns `DUPLICATE` without adding a second record.
- Same ID with a different payload returns `CONFLICT`, stores the incoming conflicting payload in a separate conflict table and preserves the original observation.
- Environment is stored with each accepted record.

## Run
```bash
python -m unittest discover -s tests -v
```

## Production blockers
The prototype does not expose HTTP endpoints and does not implement authentication, authorization, request-size/rate limits, multi-process concurrency policy, database migrations, retention, tamper-resistant audit, encryption-at-rest policy, backup/restore or operational telemetry. Do not expose it to a network or connect it to SAP targets before those controls and tests are implemented.
