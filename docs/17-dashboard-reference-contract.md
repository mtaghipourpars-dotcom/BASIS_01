# 17 — Dashboard Reference Lock and Deterministic Build Contract

**Normative UI reference:** `SRC/dashboard.png`  
**Git blob SHA:** `733275240a0ad83332614cfb16a12ccba5706fcc`  
**Reference URL:** https://github.com/mtaghipourpars-dotcom/BASIS_01/blob/main/SRC/dashboard.png  
**Rule:** This file is the single source of truth for dashboard appearance. Do not approximate the layout from generic dashboard conventions. When the reference image changes, review the blob SHA and update this contract deliberately.

## 1. Determinism rules

1. No developer or code-generation agent may invent fields, KPI definitions, labels, routes, statuses, data, thresholds, API endpoints, or environment names.
2. Use source evidence only for claims it actually supports. A transaction screenshot is not proof of a supported programmatic interface or polling frequency.
3. Separate the **visual reference** from the **runtime data source**. The reference fixes appearance; validated adapters provide runtime values.
4. Keep the existing repository framework and conventions after recording them. Do not introduce a competing frontend stack without an explicit architecture decision.
5. All unverified or synthetic values must be visibly labelled DEMO. Never present the numbers shown in the reference as live system values by default.
6. Missing, stale, unsupported, unauthorized and failed collection are separate states. None may silently become healthy, zero, or an empty alert list.
7. All dashboard widgets must consume the same canonical normalized data and shared rule engine. No widget may calculate a competing status independently.
8. Every displayed LIVE number/event must trace to a source, observation time, collection time, environment, quality, freshness and definition/rule version.
9. Phase 1 is read-only. No dashboard interaction may trigger SAP configuration, restart, cancellation, transport import, job modification, unlock, or remediation.

## 2. Locked visual layout

Build at the reference aspect ratio first, then implement responsive behavior without changing the desktop hierarchy.

### Global shell
- Full-viewport application; dark navy top header; dark navy vertical navigation on the left; light blue-white workspace.
- Top header: SAP/product mark at far left; product title and tagline; right-side time/date and connection indicator; notification control; user/account menu; settings.
- Navigation: Persian labels, line icons, blue active row, consistent vertical rhythm. Bottom-left help/note panel remains within the sidebar.
- RTL is the default document direction. Use explicit LTR isolation for SAP IDs, technical tokens, numeric timestamps and mixed-script labels where needed.

### Hero
- Main workspace starts with a wide dark-blue server-rack banner.
- Greeting and one-line system status are left-aligned within the RTL content region as shown in the reference.
- Brand slogan/logo block is on the opposite end of the banner.
- Use the approved local asset if the repository contains one; otherwise use a local image committed with license metadata or a CSS fallback. No runtime hotlink dependency.

### Grid row 1
Three adjacent cards:
A. **وضعیت کلی محیط‌ها**: environment subcards DEV, QAS, PRD; each has state badge and counts for systems, instances and databases.
B. **خلاصه وضعیت کل محیط**: four state totals in order healthy, warning, critical, unknown, with icon, count and Persian label.
C. **وضعیت دسترسی سیستم‌های حیاتی**: four domains in order SAP Systems, Database, File Systems, Network. Circular percentage is permitted only when an approved formula exists; otherwise use a visibly unavailable state in the same visual slot.

### Grid row 2
- Left wide panel: **هشدارها و رویدادهای مهم** with severity icon, title, system/component, event summary, timestamp, priority and row drill-down; include “مشاهده همه هشدارها”.
- Right panel: **عملکرد و ظرفیت کلیدی**; two-column/three-column KPI grid as space permits: CPU, Memory, Disk Usage, response time, Work Processes, Database; below it, resource trend chart with CPU/Memory/Disk legend and explicit time window.

### Grid row 3
- Left: **دسترسی سریع به حوزه‌های تخصصی**, arranged as four-column tiles on reference desktop, preserving order from the reference: systems/instances, database, performance/bottlenecks, logs/processes, errors, capacity/forecast, security, backup/recovery, communications/interfaces, transports, monitoring agent, reports/analysis.
- Right upper/lower region: **سلامت محیط‌ها (جزئیات سریع)** matrix by environment and domain; **آخرین فعالیت‌ها** compact timestamped event list.
- Keep relative widths, panel hierarchy, card borders, spacing, blue icon accents and typography consistent with the reference. Do not add extra cards to the initial dashboard without updating the reference contract.

## 3. Visual geometry and responsive contract

The committed reference is a 1536×1024 screenshot. Treat that as the baseline viewport for visual regression. Preserve major panel boundaries, relative widths, order, alignments, and whitespace before micro-adjusting icon pixels.

Required visual checkpoints at 1536×1024:
- Header spans full width; sidebar occupies a narrow fixed left rail.
- Hero spans the main content width below the header.
- Three summary cards occupy the first content row.
- Alerts panel occupies the left side of the middle row; performance panel occupies the right side.
- Quick-link panel occupies lower left; health matrix and activity occupy lower right.
- No overlap, clipped Persian text, unintentional scrollbar, or broken chart legend.

Responsive variants:
- At narrower widths, preserve information order and hierarchy; collapse navigation into a drawer and stack cards. Do not attempt to squeeze the 1536px layout into a phone width.
- The desktop screenshot is the visual-regression target; responsive layouts have separate accessibility/layout acceptance tests.

## 4. Canonical data ownership

Create one mapping pipeline:
**Source Adapter → Raw Evidence Envelope → Validation/Redaction → Canonical Observation → Rule Engine → Dashboard View Model → Widget**

No direct SAP GUI scraping is allowed as the runtime collection method. Existing transaction evidence guides source discovery and validation.

### Canonical status enum
`HEALTHY | ATTENTION | CRITICAL | UNKNOWN | STALE | NOT_SUPPORTED`

Severity in an event is separate from target health. A warning event may coexist with a healthy current metric; a missing source may make a widget UNKNOWN even when there is no alert.

### Mandatory provenance per displayed value
- environment and stable target ID
- metric/event ID and definition version
- numeric value and unit, or event fields
- source adapter ID/version and source object
- observed-at and collected/received-at timestamps with timezone
- quality/freshness and coverage status
- rule/threshold version if a state is calculated
- evidence reference

### Required metric-definition registry
Before a metric can be shown as LIVE, register: metric ID, definition, unit, aggregation, valid range, source, polling interval, stale-after limit, threshold/rule, environment applicability, owner, sensitivity classification and test fixture.
Do not infer formulas for the four access rings, response time, work-process ratio, database percentage, or overall status.

## 5. Source evidence mapping and limitations

Use the artifacts in `SRC/` to validate the following areas:
- `SM51.pdf`: instance inventory snapshot.
- `SM50.pdf`, `SM66.pdf`: work-process snapshots, not continuous history.
- `ST06.pdf` and `ST06-01.pdf`–`ST06-03.pdf`: OS/host metric evidence and units.
- `ST03N.pdf`, `ST03N-01.pdf`, `ST03N-02.stats`, `ST03N-03.stats`: workload period/aggregation and possible trend evidence.
- `SM37.pdf`: bounded job status/history; redact job/user-sensitive fields.
- `ST22.pdf`, `SM21.pdf`, `SM13.pdf`: bounded dump/system-log/update event evidence; do not ingest unrestricted payloads.
- `SM12.xlsx`, `SM04.xlsx`: lock/session evidence; minimize and redact identity data.
- `RZ20.pdf`: monitoring alert context; absence of an alert is not proof of health.
- `DB12.pdf`, `DB12-01.png`–`DB12-11.png`: backup evidence. Backup success is not restore-test evidence.
- `SMGW.pdf`: gateway evidence.
- `STMS.pdf`: transport context; Phase 1 read-only.
- `sapchart_dbg.txt`, `test.txt`: do not use until their purpose/content is explicitly reviewed.
- `dashboard.png`: visual specification only; its values are not operational evidence.

Important: the file listing proves the artifacts exist; it does not itself validate every value inside them or prove a supported API. Before marking any metric LIVE, record the reviewed file/page/row, system and time context, source field, unit, and validation result in the source coverage matrix.

## 6. Required machine-readable project artifacts

Maintain these files and keep them consistent:
1. `docs/16-dashboard-build-plan.md` — human-readable sequence and acceptance gates.
2. `docs/17-dashboard-reference-contract.md` — this visual/data contract.
3. `docs/metric-registry.yaml` — canonical metric definitions; no unapproved LIVE KPI.
4. `docs/source-coverage.yaml` — each metric/event → source → interface → authorization → freshness → evidence → status.
5. `docs/dashboard-widgets.yaml` — widget ID → title/order/layout → view-model fields → empty/error states.
6. `docs/routes.yaml` — route IDs, Persian labels, order, implemented status and authorization.
7. `schemas/observation.schema.json` — machine-validated envelope schema.
8. `fixtures/demo/` — explicitly synthetic data only.
9. `tests/visual/` — screenshot baseline and visual-regression instructions.
10. `docs/acceptance-results.md` — test command, commit SHA, result and reviewer.

Do not duplicate metric definitions in widget code. These registry files are authoritative; generated code should derive bindings from them.

## 7. Ordered implementation gates

**Gate 0 — Inventory:** inspect actual source tree, framework, build commands and deployment target. Record facts, not assumptions.  
**Gate 1 — Evidence extraction:** review all SRC PDFs/images/spreadsheets/text/stats, record capture times, system identity (pseudonymize if needed), columns, units, filters and coverage. Binary artifacts must be actually parsed, not inferred from filenames.  
**Gate 2 — Registries:** create route, widget, metric and source-coverage registries; mark unknown fields explicitly BLOCKED.  
**Gate 3 — Contract:** schema validation, status/freshness rules, redaction and provenance tests pass.  
**Gate 4 — Visual shell:** implement reference layout with DEMO label and deterministic fixture data.  
**Gate 5 — Widgets:** implement components in locked order; no LIVE value without registry approval.  
**Gate 6 — Source adapters:** implement only validated, supported, read-only interfaces; no credentials in frontend or repository.  
**Gate 7 — Unified backend:** normalize, deduplicate, retain conflicts, report collector health and coverage; secure API with authentication/authorization.  
**Gate 8 — Integration:** all widgets consume one API/view-model pipeline; no hard-coded metric values in production build.  
**Gate 9 — Regression:** compare 1536×1024 screenshot to the locked reference; run responsive, RTL, accessibility and failure-state tests.  
**Gate 10 — LIVE pilot:** approve least-privilege access, polling load, data redaction, source coverage and Basis owner sign-off.

No gate may be skipped. A failing gate blocks later LIVE claims.

## 8. Visual regression and acceptance

- Use the repository's existing framework/test runner after Gate 0; do not assume Playwright/Vitest/etc. before inventory.
- Capture at exactly 1536×1024, same browser/device scale, with deterministic DEMO fixture and fixed test clock.
- Compare layout and panel bounds, card order, major spacing, typography, RTL alignment, icon placement and chart dimensions.
- Mask only dynamic date/time or explicitly dynamic areas; never mask structural differences.
- Set an agreed pixel-difference tolerance after the first baseline run and document it; do not silently loosen it to hide mismatches.
- Also verify 1280×800, tablet and mobile separately.
- Acceptance requires all controls functional, no fake LIVE labels, no console errors, no clipped text, and all tests passing.

## 9. Hard blockers — ask the owner only if the repo cannot answer

Do not ask for information already present in the repository. Inspect the repository and SRC first. If unresolved after evidence review, request only:
- frontend/runtime/deployment facts not recorded in source control;
- access to a sanitized, approved live test endpoint and a least-privilege test account, if LIVE integration is requested;
- owner-approved KPI formulas/thresholds that cannot be established from source evidence;
- a decision on any text that remains unreadable/ambiguous in the reference.

Until then, implement the visual shell and DEMO path without guessing; mark the relevant LIVE widgets blocked.
