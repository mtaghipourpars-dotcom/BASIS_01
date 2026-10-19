# Phase 1 Target Design — Evidence-Driven Baseline

## 1. Objective

Deliver a read-only SAP Basis monitoring service that consolidates verified observations from SAP and host sources, presents their current state with freshness and confidence, and links every alert to evidence. The system must not execute administrative actions in Phase 1.

## 2. Logical components

```text
SAP systems / database / operating systems / existing monitoring
             |
             v
Source adapters (SAP Host Agent / supported SAP interfaces /
 approved read-only ABAP endpoint / OS collector / CCMS import)
             |
             v
Collector scheduler + bounded queue + retry/backoff
             |
             v
Authenticated ingestion API
             |
             v
Schema validation -> normalization -> deduplication -> redaction
             |
             +--> time-series observations
             +--> event/alert store
             +--> source coverage & collector-health store
             |
             v
Freshness evaluator + deterministic rule engine
             |
             v
API/read model -> dashboard, system detail, event drill-down, reports
```

The diagram describes logical boundaries, not a claim that a specific deployment technology or SAP interface has been selected.

## 3. Source strategy

Selection order for each metric:
1. Existing supported monitoring interface or enterprise monitoring export, if already deployed and authorized.
2. SAP Host Agent interface for supported host/instance facts where available.
3. Supported SAP standard API/interface appropriate to the installed release.
4. Minimal custom ABAP read-only service for facts not covered above, after security review.
5. Manual evidence only for initial baseline/acceptance; never silently present it as live monitoring.

Do not use SAP GUI automation or direct reads of undocumented SAP tables as the default production integration. Every metric needs a source adapter specification and a tested support statement.

## 4. Phase 1 collection domains

| Domain | Candidate baseline | Important limitation |
|---|---|---|
| Landscape / instances | SID, instance identity, reported state, last seen | Probe success and SM51 inventory are distinct signals |
| Host | CPU, memory, filesystem, disk I/O, uptime where supported | OS-specific collection and permissions; Linux/Windows adapters may differ |
| Work processes | Counts by state, long-running processes, timestamp | Snapshot values; thresholds need baseline and release context |
| Workload | Response/workload aggregates available from ST03N or supported interface | Aggregated workload is not equivalent to current host utilization |
| Background jobs | Recent failed/cancelled jobs and delayed/long-running jobs | Must define job scope, time window and sensitive-field redaction |
| ABAP errors | Dump and system-log event summaries | Avoid collecting full dump payloads unless approved for incident diagnostics |
| Updates / locks | Failed updates, lock count/age where supported | Raw lock/session details can expose user/business information |
| Database | Availability, capacity and performance metrics from supported DB interface | DB-specific adapter; DBACOCKPIT/DB12 views are evidence, not collection APIs |
| Monitoring alerts | Existing CCMS/RZ20 alerts where extractable | No alert does not mean healthy |
| Backup evidence | Latest observed backup/catalog state and age | Backup job success is not restore proof |
| Connectivity | ICM/Gateway/interface health where supported | Do not infer end-to-end connectivity from a single component |
| Collector health | Last success, lag, error category, queue depth, version | Monitoring must expose its own blind spots |

## 5. Observation contract

Every observation should carry:
- `schema_version`
- `observation_id` and idempotency key
- `landscape_id`, `system_id`, `instance_id` where applicable
- `metric_key` or `event_type`
- `value`, `unit`, and optional dimensions
- `source_type`, `source_name`, `source_version`
- `observed_at`, `collected_at`, `ingested_at` (UTC, RFC 3339)
- `quality`: `OK | DEGRADED | UNKNOWN`
- `freshness`: `FRESH | STALE`
- `coverage_status`: `CONFIRMED | CANDIDATE | BLOCKED | NOT_SUPPORTED`
- `redaction_profile` and rule version where relevant

A missing value must not be coerced to zero. Unknown, stale, unsupported and collection failure are separate states.

## 6. Health state evaluation

State precedence:
1. **UNKNOWN** when no valid observation exists or source coverage is unconfirmed.
2. **STALE** when last successful observation exceeds the metric-specific freshness SLO.
3. **CRITICAL / WARNING** only when a valid fresh observation crosses a documented rule.
4. **HEALTHY** only when required signals are fresh and all applicable rules pass.
5. **NOT_SUPPORTED** where the source cannot provide the metric; do not count this as healthy.

Every rule must define metric, comparator, threshold, unit, evaluation window, severity, applicability, suppression/correlation, and evidence link. Thresholds must be configurable and documented; do not invent universal SAP thresholds.

## 7. Dashboard information architecture

- **Overview:** landscape counts by Healthy / Warning / Critical / Unknown-Stale; highest-priority evidence-backed events; collection coverage and last refresh.
- **Systems & Instances:** SID, instance inventory, last-seen and state provenance.
- **Host & Capacity:** CPU, memory, filesystem, I/O and trends only where source and units are verified.
- **Work Processes & Workload:** current work-process snapshot separate from historical workload.
- **Jobs & Updates:** failed jobs, update failures and age/window.
- **Errors & Events:** ST22/SM21-derived summaries with time filter and safe drill-down.
- **Database & Backup Evidence:** database state/capacity and backup observations with explicit recoverability caveat.
- **Locks & Sessions:** aggregate-first view, restricted drill-down.
- **Connectivity & Gateway:** ICM/Gateway observations and probe provenance.
- **Monitoring Coverage:** source coverage, freshness, adapter health and unsupported metrics.
- **Audit & Configuration:** access/audit history and threshold/config version.

## 8. Security and operations

- Read-only credentials and least privilege; credentials never in repository or logs.
- TLS in transit; secrets in deployment secret store.
- Separate identities for host and SAP collectors.
- Strict allowlist of collected fields; redact usernames and business identifiers where possible.
- Request authentication, authorization by landscape/system, rate limiting and audit.
- Bounded timeouts/retries and circuit breakers; no unbounded retry loops.
- Explicit collector disable switch and clear degraded state when disabled.
- No execution, restart, configuration change, job cancellation, lock deletion, transport import or backup action in Phase 1.

## 9. Acceptance gates

Phase 1 is not complete until:
- All displayed metrics have source, unit, timestamp, freshness policy and owner.
- Unknown/stale/unavailable source cases are correctly rendered.
- Repeated ingestion is idempotent and time ordering is robust.
- Credentials and sensitive payloads do not appear in logs or repository.
- Failure tests cover SAP unreachable, host unreachable, malformed payload, timeout, stale data and collector outage.
- At least one real environment has been validated with approved read-only access; otherwise the result remains a design/mock baseline, not production-validated monitoring.
