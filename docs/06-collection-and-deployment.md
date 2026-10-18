# 06 — Collection and Deployment
Status: deployment-agnostic baseline pending target inventory.

## Polling
- Use different intervals by domain; no single high-frequency global poll.
- Configure per-source interval, timeout, concurrency, retry policy and stale threshold.
- Retry transient failures with exponential backoff and jitter; do not retry authorization failures indefinitely.
- Local buffer must have configured disk/record cap; expose oldest item age, queue depth and dropped count.
- Jitter polling across hosts to avoid synchronized load.
- Stable record IDs support duplicate-safe replay.
- Define target-load safety limits with the Basis owner before enabling collection.

## Failure categories
Keep NO_DATA distinct from zero. Map AUTH_ERROR, TIMEOUT, SOURCE_UNAVAILABLE, UNSUPPORTED, INVALID_PAYLOAD, INGEST_REJECTED and CLOCK_SKEW distinctly. Collection failures update source/collector health and freshness. Central ingestion failure must not burden SAP; buffer only within a bounded policy.

## Deployment profiles
- Development: synthetic fixtures only; no live credentials.
- Integration: DEV/QAS, isolated credentials and measured polling impact.
- Pilot: limited approved systems, monitoring of collector load, documented rollback.
- Production: only after acceptance, security sign-off, restore drill and handover.

## External configuration
Platform URL, collector ID, inventory, enabled sources, intervals, timeouts, concurrency, retry limits, buffer cap, TLS trust, secret references, retention and feature flags. Secrets must be held in an approved secret store or protected service configuration, not a committed .env file.

## Platform observability
Track poll success/failure and latency, target response codes, queue depth, oldest buffered record, ingest lag, schema rejects, duplicates/conflicts, storage growth, API latency/errors, UI errors and platform resource use.

## Release and recovery deliverables
Versioned deployment manifest/config schema; service account/role guide; TLS/rotation guide; install/upgrade/rollback instructions; platform backup/restore procedure; recovery test evidence; retention policy; health checks; release revision and dependency versions.
