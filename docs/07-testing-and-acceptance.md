# 07 — Testing and Acceptance
No production readiness claim without recorded evidence.

## Test layers
Unit tests for mapping, conversion, freshness and status rules; contract tests for schema compatibility; adapter integration for authentication/permissions/pagination/timeouts; end-to-end source-to-dashboard; resilience for network/source/central outage and replay; security tests; performance/load tests on targets; platform backup/restore.

## Mandatory scenarios
| ID | Scenario | Expected result |
|---|---|---|
| T-01 | Valid fresh observation | Stored and shown with source, timestamp and unit |
| T-02 | No observation beyond freshness limit | STALE/UNKNOWN; never green |
| T-03 | Valid explicit zero | Zero shown and distinguished from missing |
| T-04 | Unsupported metric | NOT_SUPPORTED; no fabricated value |
| T-05 | Authorization failure | Visible source failure; no infinite retry |
| T-06 | Central ingestion unavailable | Bounded buffer; target remains unaffected |
| T-07 | Duplicate replay | Idempotent; duplicate evidence available |
| T-08 | Same ID, conflicting payload | Conflict flagged and auditable |
| T-09 | Clock skew | Quality warning; original timestamp retained |
| T-10 | Malformed/wrong schema | Rejected with reason |
| T-11 | DEMO payload | Marked DEMO throughout UI/API/export |
| T-12 | Write action attempt | No Phase 1 write capability; denied |
| T-13 | Partial source coverage | Partial/unknown explicitly displayed |
| T-14 | Unit conversion | Exact expected normalized value |
| T-15 | Dashboard drill-down | Provenance and underlying evidence reachable |
| T-16 | Platform restore | State/config/history restored per policy |

## Gate M1 exit criteria
- Every displayed metric has approved definition, unit, source, interval, freshness threshold and owner.
- Each live source tested against a representative version; authorization reviewed.
- No unresolved critical/high security findings; secrets absent from Git/logs.
- Bounded outage/replay test passes and duplicate behavior is verified.
- Stale, missing, unsupported and failed-source states are visibly correct.
- Dashboard claims trace to underlying observations.
- Target polling load measured and accepted by the Basis owner.
- Install/upgrade/rollback/backup/restore guides reviewed.
- Test evidence, limitations, known defects and sign-offs accompany release.

## Evidence record
For each test record ID, build/commit, environment, target versions, date, operator, fixture/input, expected and actual result, evidence link, defect and sign-off. Design review or synthetic fixtures alone cannot mark live integration tests as passed.
