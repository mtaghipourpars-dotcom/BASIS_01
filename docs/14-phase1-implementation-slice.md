# 14 — Phase 1 Implementation Slice: Contract and Freshness

**Status:** initial executable scaffold; not production-ready and not live-connected.

## Delivered
- Dependency-free Python envelope validator for canonical metric/event records.
- Freshness evaluator with explicit UNKNOWN behavior for missing, invalid or future timestamps.
- DEMO-only sample metric fixture.
- Unit tests for explicit zero vs missing value, timezone-aware timestamps, environment separation, evidence reference and freshness.
- GitHub Actions workflow running unit tests and validating the fixture.

## Run locally
```bash
python -m unittest discover -s tests -v
python -c "import json; from app.contract import validate_observation; validate_observation(json.load(open('fixtures/demo_metric.json', encoding='utf-8')))"
```

## Deliberate boundaries
- This is a first vertical slice, not an API server, collector, database, dashboard or SAP integration.
- It validates the common envelope; production source-specific schemas, size limits, authentication, authorization, replay protection and redaction are not implemented here.
- It does not calculate HEALTHY/ATTENTION/CRITICAL. Freshness alone cannot prove target health.
- All fixture data is synthetic and must remain labelled DEMO.
- No SAP/OS credentials or network access are used by these tests.

## Next implementation gate
Add strict JSON Schema validation and event tests; then implement idempotent ingestion with duplicate/conflict handling and persistent audit before creating any target adapters. Live integration remains blocked until target versions, approved interfaces, roles, network path and load limits are evidenced.
