# 03 — Source Coverage Matrix
**All coverage below is CANDIDATE until tested on the exact installed versions.**

| Domain | Candidate source | Phase 1 stance | Caveat / proof required |
|---|---|---|---|
| Host CPU/memory/filesystems | SAP Host Agent where exposed; approved OS adapter | Candidate | Verify metrics, permissions, sampling and supported interface |
| Host network and I/O | OS-specific adapter or approved monitoring API | Candidate | OS-specific privilege and semantics |
| SAP instance availability | SAP Host Agent / supported SAP management interface | Candidate | Verify endpoint, auth and installed version |
| Work processes | Supported SAP interface or reviewed ABAP read-only service | Candidate | Define snapshot and target load |
| System log / ABAP dumps | Standard SAP API or narrow ABAP service | Candidate | Authorization, pagination, retention and sensitive data |
| Background jobs | Supported SAP job-monitoring interface or narrow ABAP service | Candidate | Minimize job/user/business details |
| Locks and updates | Supported monitoring interface or narrow ABAP service | Candidate | Inspection only; never delete |
| Database | Supported database-specific monitoring interface | Candidate | DB product/version unknown; no universal query assumed |
| Transports | Supported CTS/TMS read-only source | Candidate | Confirm controller and landscape routing |
| Backup/recovery | Backup platform API plus database evidence | Partial | Job/file alone does not prove recoverability |
| Connectivity/interfaces | Approved endpoint checks | Candidate | Owners, network zones and credentials must be defined |
| Collector health | Platform-native telemetry | MUST | Heartbeat, last success, errors, backlog, drops, version |
| Security/configuration | Approved read-only sources and platform audit | Partial | Scope after security review |

## Coverage statuses
- CONFIRMED: tested on a representative target version with evidence.
- CANDIDATE: plausible source, not tested.
- BLOCKED: access or policy prevents implementation.
- NOT_SUPPORTED: no approved source available.
- STALE: expected observations absent beyond configured threshold.

## Source record required for each metric
Metric ID/definition; source product/interface and version; target version compatibility; endpoint/operation; required role; polling interval, timeout, concurrency and expected load; sanitized sample response; normalization/unit conversion; error mapping; freshness threshold; test date, tester, result and limitations.

## Decision sequence
Inventory exact versions → inspect Host Agent and supported interfaces → document each metric/source/authorization/load → prefer standard supported APIs → assess narrow custom ABAP service for SAP-specific gaps → assess separate Linux/Windows adapters for remaining host gaps. Do not build a custom agent until this assessment is complete.
