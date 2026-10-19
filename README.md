# BASIS_01 — SAP Basis Operations Cockpit
**Phase 1: Monitoring foundation | Architecture baseline v0.2 | Status: Draft for validation**

BASIS_01 targets a multi-system landscape containing SAP S/4HANA On-Premise on Linux and SAP ECC on Windows Server. Product delivery is explicitly phased: **Monitoring → Warning → Execution & Operations**.

## Documentation
- [Target architecture](docs/01-architecture.md)
- [Phase 1 requirements](docs/02-phase1-requirements.md)
- [Source coverage matrix](docs/03-source-coverage-matrix.md)
- [Canonical data contract](docs/04-data-contract.md)
- [Security model](docs/05-security.md)
- [Collection and deployment](docs/06-collection-and-deployment.md)
- [Testing and acceptance](docs/07-testing-and-acceptance.md)
- [Operations runbook](docs/08-operations-runbook.md)
- [Decisions and open questions](docs/09-decisions-and-open-questions.md)
- [SAP evidence request](docs/10-sap-evidence-request.md)
- [SRC evidence assessment](docs/11-src-evidence-assessment.md)
- [Phase 1 target design](docs/12-phase1-target-design.md)
- [SRC artifact register](docs/13-src-file-register.md)
- [Source evidence directory](SRC/)

## Non-negotiable rules
1. Evidence before status: every value has a source, timestamp, quality, freshness and drill-down.
2. Unknown/stale/unsupported data is never shown as healthy.
3. Synthetic examples are always labeled DEMO; LIVE is allowed only after source validation.
4. Phase 1 is read-only on SAP and OS targets. No restart, configuration change, job cancellation, lock deletion, transport import or remediation.
5. Monitoring facts, Phase 2 warnings/diagnosis and Phase 3 execution remain distinct.
6. Assess SAP Host Agent and supported interfaces before building a custom agent.
7. Shared canonical contract, with separate Linux and Windows adapters where needed.
8. Transaction screenshots and exports are baseline evidence, not proof of an automatable supported API.
9. Backup completion is not proof of recoverability; report restore-test evidence separately.

## Current status
This repository establishes a proposed architecture and requirements baseline informed by the artifact inventory under SRC. The source files must be content-reviewed and reconciled with their system, time window, units and filters before any individual metric is marked confirmed. Target servers are not currently accessible, so exact source coverage, compatibility, load and end-to-end behavior are not validated. No production credentials or sensitive exports belong in Git.

## Phase gates
- **M1 Monitoring:** trusted read-only collection, normalization, freshness/quality, dashboard and evidence drill-down.
- **M2 Warning:** thresholds, trends, correlation, deduplication and prioritization.
- **M3 Execution & Operations:** approval-controlled workflows, preconditions, audit, result verification and rollback/compensation where safe.

A rendered dashboard or synthetic fixture is not evidence that Phase 1 is complete.
