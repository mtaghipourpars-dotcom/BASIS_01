# 09 — Decisions, Assumptions and Open Questions

## Baseline decisions
- D-001: Product phases remain Monitoring, Warning, Execution & Operations.
- D-002: Phase 1 is read-only on SAP and OS targets.
- D-003: Unknown/stale/unsupported is never rendered healthy.
- D-004: Every displayed measurement needs provenance and freshness.
- D-005: Evaluate Host Agent and supported SAP interfaces before custom agent development.
- D-006: Shared canonical contract; separate Linux/Windows adapters as needed.
- D-007: DEMO/TEST/LIVE are separated throughout the stack.
- D-008: No KPI/availability percentage without a documented formula/source.
- D-009: No generic table reader, arbitrary RFC proxy, remote shell or write endpoint.
- D-010: Architecture is proposed, not yet validated against live systems.

## Assumptions to validate
The landscape includes S/4HANA On-Premise on Linux and ECC on Windows Server, with DEV/QAS/PRD tiers. Actual SIDs, versions, database products, network paths, identities and ownership remain unknown.

## Blocking questions
1. Exact SAP product/release, SAP_BASIS/SP, kernel release/patch and Host Agent version?
2. Database product/version for each system?
3. Host Agent installed, patched and reachable? Which supported interfaces are approved?
4. Existing monitoring tools (Solution Manager, Focused Run, third-party monitoring, backup tools)?
5. Are outbound connections allowed, or must collectors push through a proxy/DMZ?
6. Runtime/hosting constraints: Linux VM, Windows VM, containers/Kubernetes or no container runtime?
7. Storage preference, retention, HA, backup and recovery objectives?
8. Identity source: AD/LDAP, SSO, local accounts or certificate-based collector identity?
9. Which metrics are mandatory for the first usable release, and who owns each?
10. Accepted polling intervals and target-load limits?
11. Sensitive fields and retention/export policy for dumps, job data and usernames?
12. UI language, RTL, roles, audit and reporting needs?
13. Approved test window and representative DEV/QAS system?
14. Which sanitized transactions/API outputs can be supplied?

## Risks and mitigations
- Unsupported API assumptions: prove source coverage by version before coding.
- Excessive polling: low-frequency pilot, hard limits and measured impact.
- Stale data appears healthy: freshness contract and mandatory tests.
- ABAP service becomes privileged gateway: narrow allowlist and reviewed authorization.
- Sensitive data leaks: minimize, redact, scan repository and logs.
- UI implies later-phase capabilities: phase-gated navigation and no fake actions.
