# 04 — Canonical Data Contract
Version 0.1 draft. Keep the contract versioned and backward-compatible.

## Principles
- Preserve source meaning and identifiers while normalizing units/names.
- Distinguish source observation time from central receipt time.
- Missing, invalid and unsupported differ from numeric zero.
- Every observation carries provenance, quality, freshness and environment.
- Do not store secrets or unrestricted sensitive log payloads in standard metric records.

## Metric record example
    {
      "schema_version": "1.0",
      "record_type": "metric",
      "record_id": "demo-host-cpu-host01-20260101T100000Z",
      "environment": "DEMO",
      "target": {
        "system_id": "S4D",
        "sid": "S4D",
        "environment_tier": "DEV",
        "component": "host",
        "host_id": "host-01",
        "os_family": "linux"
      },
      "metric": {
        "id": "host.cpu.utilization",
        "value": 42.7,
        "unit": "percent",
        "aggregation": "sample",
        "definition_version": "1"
      },
      "source": {
        "adapter_id": "linux-adapter",
        "adapter_version": "0.1.0",
        "source_type": "DEMO_FIXTURE"
      },
      "observed_at": "2026-01-01T10:00:00Z",
      "received_at": "2026-01-01T10:00:02Z",
      "quality": {
        "status": "VALID",
        "flags": [],
        "freshness": "FRESH"
      },
      "evidence_ref": "demo-evidence-001"
    }

## Event record example
    {
      "schema_version": "1.0",
      "record_type": "event",
      "record_id": "demo-job-failed-001",
      "environment": "DEMO",
      "target": {
        "system_id": "ECCQ",
        "sid": "ECCQ",
        "environment_tier": "QAS",
        "component": "background_job"
      },
      "event": {
        "event_type": "job.execution",
        "status": "FAILED",
        "severity": "HIGH",
        "title": "Demonstration job failure",
        "description": "Synthetic fixture; not a live incident."
      },
      "source": {
        "adapter_id": "demo-fixture",
        "adapter_version": "0.1.0",
        "source_type": "DEMO_FIXTURE"
      },
      "first_observed_at": "2026-01-01T09:55:00Z",
      "last_observed_at": "2026-01-01T10:00:00Z",
      "received_at": "2026-01-01T10:00:02Z",
      "quality": {
        "status": "VALID",
        "freshness": "FRESH"
      },
      "evidence_ref": "demo-evidence-002"
    }

## Enumerations
- environment: DEMO, TEST, LIVE.
- quality.status: VALID, INVALID, PARTIAL, UNAVAILABLE.
- quality.freshness: FRESH, STALE, UNKNOWN.
- computed status: HEALTHY, ATTENTION, CRITICAL, UNKNOWN, STALE, NOT_SUPPORTED.
- severity: INFO, LOW, MEDIUM, HIGH, CRITICAL, UNKNOWN.
- source_type: SAP_HOST_AGENT, SAP_STANDARD_API, ABAP_READ_ONLY_SERVICE, LINUX_ADAPTER, WINDOWS_ADAPTER, BACKUP_PLATFORM_API, DEMO_FIXTURE.

## Idempotency
Prefer source-issued stable IDs. Otherwise derive deterministic keys from source, target, metric/event and source timestamp/window. Same key and same payload is a no-op. Same key with conflicting payload must be flagged and retained for investigation, not silently overwritten.

## Proposed API outline
- POST /api/v1/observations — authenticated collector ingestion.
- GET /api/v1/landscape — registered systems and computed states.
- GET /api/v1/systems/{systemId} — system detail.
- GET /api/v1/metrics?systemId=&metricId=&from=&to= — bounded time-series query.
- GET /api/v1/events?systemId=&severity=&from=&to= — observed events.
- GET /api/v1/collectors/health — collector freshness/errors.
- GET /api/v1/coverage — source coverage.
- GET /health/live and /health/ready — platform health, no secrets.

Before production, define pagination, maximum query ranges, payload limits, authentication, rate limits and request IDs. A percentage cannot be called availability until its formula and source are documented.
