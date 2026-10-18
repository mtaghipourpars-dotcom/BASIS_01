# 01 — Target Architecture
Status: proposed baseline; validate against exact product versions and security constraints.

## Purpose
Deliver one evidence-driven operational view across SAP systems and hosts without confusing a collection failure with target health.

## Logical flow
Target SAP systems, databases and Linux/Windows hosts → read-only source adapters → authenticated ingestion API → schema validation and normalization → metric/event storage → deterministic status and freshness evaluator → read API → web cockpit.
A separate monitoring-of-monitoring path records collector heartbeat, last success, errors, backlog, rejected records and adapter version.

## Components
- **Source adapters:** use documented and supportable read-only interfaces. Report their own health/version.
- **Ingestion:** authenticate each collector, validate schema, apply payload/rate limits and protect against replay.
- **Normalization:** map source-specific records into a versioned canonical contract while preserving provenance and sanitized evidence references.
- **Storage:** logically separate time-series measurements, events, inventory/configuration and audit records. Select technology after volume, retention, HA and team constraints are known.
- **Status evaluator:** emit HEALTHY, ATTENTION, CRITICAL, UNKNOWN, STALE or NOT_SUPPORTED using documented rules. Missing data is never numeric zero.
- **Read API/UI:** landscape status, observations, trends, freshness and evidence. Do not present a hypothesis as confirmed root cause.
- **Monitoring of monitoring:** collector health, ingestion lag, schema rejects, dropped records, storage growth and API health.

## Trust and failure boundaries
1. Collector outage changes collector/source status; it does not prove the SAP target is down.
2. Temporary network loss must not block or burden the target. Any local queue is bounded and observable.
3. Duplicate delivery is expected; ingestion must be idempotent. Conflicting payloads for the same stable ID are flagged, not silently overwritten.
4. Preserve both source observation time and platform receipt time; use UTC internally and flag clock skew.
5. Do not publish a KPI until its definition, unit, source, sampling interval, aggregation and owner are documented.
6. Phase 1 records observations; Phase 2 adds warning/correlation; Phase 3 adds separately secured execution.

## Deployment units
Central API/ingestion, normalization/status worker, persistent store, web UI, collectors, secret/certificate management and audit logging. They may initially be deployed together, but their responsibilities and interfaces should remain explicit. Avoid premature microservice proliferation.

## Source selection sequence
1. Inventory SAP releases, kernel, SAP Host Agent, OS and database versions.
2. Verify installed Host Agent capabilities and supported interfaces.
3. Map each required metric to an approved source, authorization, polling interval and sanitized sample.
4. Prefer supported standard interfaces.
5. For SAP-specific gaps, assess a narrow reviewed ABAP read-only service.
6. For remaining host gaps, assess separate low-privilege Linux/Windows adapters.
7. Mark unsupported metrics NOT_SUPPORTED; never fabricate values.

## Phase boundaries
- **Phase 1 Monitoring:** observations, inventory, history, freshness, data quality and drill-down.
- **Phase 2 Warning:** configurable thresholds, trends, correlation, deduplication, routing and acknowledgement.
- **Phase 3 Execution & Operations:** controlled action catalog, authorization/approval, preconditions, idempotency, audit, result verification and rollback strategy.
