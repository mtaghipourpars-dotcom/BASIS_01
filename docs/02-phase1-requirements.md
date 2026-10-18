# 02 — Phase 1 Monitoring Requirements
Version 0.1. Priority labels: MUST and SHOULD.

## Objective
Operators can identify which systems are observed/reachable, inspect evidence-backed operational events, review supported resource/performance trends, assess data freshness and drill down to source evidence.

## In scope
- Inventory of systems, instances, environment tier, OS family, database type, criticality and ownership.
- Host CPU, memory, filesystem, disk I/O and network measures where supported.
- SAP instance/process and selected work-process indicators where a supported interface is confirmed.
- Database measures only for explicitly supported products/interfaces.
- Background job status/duration where safe read-only access is confirmed.
- ABAP dumps/system logs, locks/updates and transport status only after source and authorization validation.
- Collector health, freshness, collection errors, schema compatibility and ingestion backlog.
- Dashboard and detail views, filters, trends, evidence drill-down, bounded export.
- Clear DEMO/TEST/LIVE separation.

## Out of scope
- Automated warning delivery/escalation and advanced correlation (Phase 2).
- Asserted root-cause diagnosis or automated remediation.
- SAP/OS writes: restarts, profile changes, job release/cancel, lock deletion, transport import, user changes or database commands.
- Generic RFC proxy, arbitrary table reader, unsupported direct database queries or GUI screen scraping as a production integration.
- Claims that a backup file/job proves recoverability; recovery requires independently defined restore-test evidence.

## Functional requirements
- FR-01 Inventory: register system, SID, tier, instances/hosts, OS, database, owner and criticality.
- FR-02 Source registry: each source defines supported metrics, interval, timeout, privileges and adapter version.
- FR-03 Contract: every observation carries metric ID, value, unit, target, source, observed time, received time, quality and schema version.
- FR-04 Freshness: configurable expected interval/stale threshold; missing data becomes UNKNOWN or STALE.
- FR-05 Deterministic status rules with rule version and contributing evidence.
- FR-06 Trends show time range, units, aggregation and gaps; do not interpolate missing observations as healthy.
- FR-07 Evidence link for every displayed event/observation.
- FR-08 Collector health: heartbeat, last successful poll, errors, queue depth, retry and dropped count.
- FR-09 Read-only target access, TLS, secret rotation, audit and least privilege.
- FR-10 DEMO/TEST/LIVE enforced in API, storage, UI and export.
- FR-11 Bounded retry/buffer, duplicate-safe replay and controlled shutdown.
- FR-12 Monitor platform health, API latency/errors, storage and ingestion lag.
- FR-13 Audit configuration changes, privileged access and exports.
- FR-14 Export filtered observations with time range, unit, quality and environment.

## Non-functional requirements
- Bound target load using polling intervals, timeouts and concurrency.
- Never allow unbounded retries or queues.
- UTC timestamps internally; preserve source timestamp/timezone when supplied.
- No secrets in logs, fixtures, screenshots or Git.
- Installation, upgrade, rollback and platform backup/restore are repeatable and documented.
- Every displayed value exposes provenance and freshness.

## Initial dashboard
1. Landscape counts by HEALTHY, ATTENTION, CRITICAL, UNKNOWN/STALE.
2. Important observed events: severity, target, component, first/last observed, trend where available and evidence.
3. Performance/capacity trends with units and thresholds only when sourced and approved.
4. Data trust: last successful collection, freshness, source health, rejects and coverage.
5. Navigation to systems, performance, database, jobs/processes, errors/locks, capacity, backup evidence, security, connectivity, transports and collectors. Unimplemented domains must be marked unavailable, not simulated as live.
