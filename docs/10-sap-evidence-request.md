# 10 — SAP Evidence Request Checklist
Architecture can progress without server access, but source selection and implementation compatibility cannot be finalized without sanitized evidence. Do not send passwords, private keys, tokens, personal data or unrestricted production logs.

## Minimum evidence package
1. System inventory: environment tier, SID, SAP product/release, SAP_BASIS/SP, kernel release/patch, OS/version, database product/version, instance count and host role. Hostnames may be consistently pseudonymized.
2. SAP Host Agent version/status per host and installed documentation/supported-interface list.
3. Existing monitoring products, approved interfaces and network routes.
4. Read-only technical roles available by purpose; never provide credentials.
5. Sanitized monitoring screen exports showing required indicators and current thresholds.

## Candidate transactions for discovery
Availability and output depend on release, configuration and authorization. These are aids for evidence gathering, not a promise that production monitoring will automate each transaction directly.

- SM51 — application server/instance inventory and status.
- SM50 / SM66 — work-process snapshots.
- SM37 — background job status and duration.
- ST22 — ABAP dump overview.
- SM21 — system log.
- SM12 — lock entries, inspection only.
- SM13 — update records/status, inspection only.
- ST03N — workload/performance analysis.
- ST06 — OS monitoring where configured.
- DBACOCKPIT — database monitoring, database-specific.
- RZ20 — CCMS monitoring where used.
- STMS — transport overview; no import or execution.
- DB12 or backup-tool views — backup history, not proof of recoverability.
- SMICM / SMGW — only for approved connectivity diagnostics and sanitized outputs.

Do not enable traces or perform mass exports without Basis owner approval. Avoid exporting user IDs, job logs, dumps or business payloads unless required and sanitized. Never export license keys.

## Host/database evidence
- Linux distribution/version, service manager and approved host-metric interface.
- Windows Server version, service identity model and approved performance-counter/management interface.
- Database product/version, supported read-only monitoring interface, metric catalogue and minimum privileges.
- Backup platform/API, job status, retention and last restore-test evidence if available.

## Preferred sanitized package
- system-inventory.csv
- host-agent-inventory.csv
- metric-source-candidates.csv
- representative screenshots/PDFs with sensitive information redacted
- one successful and one failed sanitized response for each candidate API
- short description of security/network restrictions

## Decisions supported by this evidence
Confirmed/candidate/blocked coverage per metric; Host Agent sufficiency; ABAP service gaps; Linux/Windows adapter needs; polling intervals and load limits; authorization/network flow; implementation order and test fixtures.

Never commit credentials or sensitive exports to this repository.
