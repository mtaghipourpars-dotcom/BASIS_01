# 08 — Operations Runbook (Phase 1)
## Daily checks
- Review UNKNOWN/STALE targets before assuming they are healthy or failed.
- Check last successful poll, source errors, collector heartbeat, ingest lag and oldest buffered record.
- Check platform storage/resources, API health and certificate/secret expiry.
- Review schema rejects, conflicting duplicates and dropped-record counters.
- Confirm DEMO data is never shown as LIVE.

## Triage
1. Check data freshness. If stale, inspect collector health, connectivity, authentication, queue and ingestion.
2. Separate target health from lack of observation; compare independent evidence.
3. Inspect source and receipt timestamps, sanitized evidence, source/adapter version and error category.
4. Verify that the metric is supported for the installed version.
5. If target load exceeds agreed limits, reduce/disable polling through approved platform configuration and notify the Basis owner.
6. Record findings and follow the approved change process. Phase 1 does not remediate the target.

## Disable a collector safely
Disable the affected source using approved platform configuration; record who/when/why and impacted metrics; confirm polling stopped and load returned to baseline; ensure UI shows STALE/UNKNOWN; re-enable only after source, credentials and load are reviewed.

## Incident evidence
Capture incident ID, system, source/adapter version, first/last observed, timestamps, sanitized payload, collector health, error category, recent config changes and impact. Never attach credentials or unredacted sensitive dumps.

## Release procedure
Review change/threat model; run unit/contract/integration tests; deploy to development first; validate data quality, load and rollback; promote through controlled environments; preserve release notes, test evidence and configuration diff.

This runbook does not authorize SAP restart, profile changes, lock deletion, job cancellation, transport import or database/OS remediation commands.
