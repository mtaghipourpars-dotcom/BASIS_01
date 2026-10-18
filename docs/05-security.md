# 05 — Security and Access Model
Default: least privilege, read-only collection, explicit trust boundaries.

## Threats
Protect SAP/host availability, credentials, operational logs, configuration details and monitoring integrity. Threats include stolen collector credentials, spoofed/replayed observations, excessive polling, malicious payloads, platform compromise and sensitive data leakage.

## Phase 1 controls
- Dedicated read-only target identities, with minimum authorizations per metric domain.
- No shared human accounts and no credentials, tokens, private keys or production endpoints in Git.
- TLS with certificate validation; never disable certificate verification.
- Separate identities/secrets by environment and rotate them.
- Restrict collection ports to approved network zones.
- Request timeouts, concurrency/payload limits, allowlisted operations and rate limiting.
- Sanitize errors and sensitive fields; restrict access to dumps, job logs and user identifiers.
- Audit collector registration, configuration changes, privileged access, credential rotation and exports.
- Encrypt secrets and sensitive stored data per deployment policy; define retention/deletion.
- Pin/review dependencies and maintain a release/dependency manifest.
- Enforce DEMO/TEST/LIVE separation in API, storage, UI and export.
- Disable write-capable commands and endpoints in Phase 1; hiding a button is insufficient.

## Custom ABAP service guardrails
Only if supported interfaces do not cover a required metric: narrow allowlist of read operations, explicit authorization checks, bounded pagination/results/runtime, sanitized errors and audit. No arbitrary table names, function names, SQL, dynamic code or generic RFC/table-read proxy. Use normal SAP change and transport controls; test load in nonproduction.

## OS collector guardrails
Prefer Host Agent or approved enterprise monitoring APIs where adequate. Any custom adapter uses a dedicated low-privilege service account, no interactive login, allowlisted metrics, bounded resources and no remote arbitrary shell commands. Do not collect environment variables or full process command lines by default.

## Phase 3 boundary
Execution needs a separate threat model, action catalog, RBAC/approval, precondition checks, idempotency, immutable audit, result verification, timeout behavior and rollback/compensation. Phase 1 credentials must never grant Phase 3 permissions.

## Security acceptance
Security owner signs off network flows, target roles, secrets, logging/retention, patching, backup/restore and incident response before any live pilot.
