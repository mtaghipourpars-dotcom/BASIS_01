# 16 — Dashboard Build Plan (Machine-Executable Roadmap)

**Status:** implementation specification; visual reference supplied by the project owner.  
**Target:** Persian-first, RTL SAP Basis Operations Cockpit.  
**Evidence rule:** screenshot is a visual reference, not evidence that displayed values, states, charts or integrations are live.

## 1. Readiness decision

The team can begin the UI shell and deterministic DEMO experience now. It is **not ready for a truthful LIVE dashboard**: target inventory, source coverage, metric definitions, thresholds, approved API/authentication, retention and representative live responses remain unverified.

Ready now: screenshot-based information architecture; canonical observation-envelope draft; freshness semantics; DEMO fixture; contract validation; local SQLite idempotency prototype; read-only security boundary.

Blocking LIVE data: exact SAP/OS/database versions; approved interfaces per metric; formulas, units, intervals, thresholds and freshness limits; actual inventory and ownership; authenticated API, RBAC, audit and redaction; sanitized successful/failed source examples and tests. Until explicitly confirmed, all screenshot numbers are DEMO.

## 2. Visual acceptance contract

Use the supplied image as the composition and hierarchy reference. Do not silently replace it with a generic admin template.

### Desktop composition
1. Fixed dark navy top bar: SAP/product identity, tagline, date/time, cockpit/collection indicator, notifications, user menu and settings.
2. Fixed dark navy left navigation: icon + Persian label, selected item bright blue, lower help/note panel.
3. Main workspace with dark blue server-room hero banner, greeting and status subtitle.
4. First row: environment overview (DEV/QAS/PRD, systems/instances/databases); overall status counts; vital-domain cards (SAP Systems, Database, File Systems, Network).
5. Main row: important alerts/events table on the left; CPU, memory, disk, response time, work-process and database cards plus resource trend chart on the right.
6. Lower row: quick links, environment health matrix, recent activity list.
7. Use restrained borders/shadows, blue accent, semantic status colors, compact typography and clear Persian RTL alignment.

### Responsive behavior
- Desktop: fixed sidebar; alert/performance areas in two columns.
- Tablet: sidebar collapses to icon rail/drawer; cards wrap into two columns.
- Mobile: drawer navigation; cards stack; tables become row cards or horizontally scroll with key fields visible.
- RTL applies to layout, labels, tables and legends. Technical identifiers/timestamps may use LTR isolation.
- Use a locally licensed/approved hero image or CSS gradient fallback; do not hotlink unapproved imagery. Brand assets require authorization.

## 3. Information architecture

Implement these routes or explicit placeholders:
1. صفحه اصلی
2. سیستم‌ها و اینستنس‌ها
3. عملکرد و گلوگاه‌ها
4. پایگاه داده
5. لاگ‌ها و پردازش‌ها
6. خطاها و نقل‌قول‌ها — confirm wording; screenshot text may be ambiguous
7. ظرفیت و پیش‌بینی — Phase 1 trends only; advanced forecasting/correlation is Phase 2
8. امنیت
9. پشتیبان‌گیری و بازیابی
10. ارتباطات و رابط‌ها
11. انتقال‌ها (Transports)
12. زیرساخت پایش (Agent)
13. گزارش‌ها و تحلیل‌ها
14. تنظیمات

An unimplemented route must clearly say “در دسترس نیست / Not implemented”; it must not show fake LIVE data.

## 4. Canonical UI view models

UI components consume typed view models, never adapter-specific payloads directly.

- EnvironmentSummary: environment ID, computed state, system/instance/database counts, freshness and coverage.
- StatusCounts: healthy, attention, critical, unknown, stale and not-supported counts plus snapshot time.
- AccessDomainStatus: domain ID, state, optional percentage only if its formula is documented, freshness and evidence reference.
- AlertRow: stable event ID, severity, title, target/component, first/last observed timestamps, priority, environment and evidence reference.
- MetricCard: metric ID, value, unit, aggregation, threshold state, observed/received timestamps, freshness, source and evidence.
- SeriesPoint: timestamp, numeric value, unit, quality and source reference.
- CollectorHealth: collector ID/version, last attempt/success, errors, queue depth, lag, dropped/rejected counts.
- RecentActivity: event ID, title, target, timestamp, severity and evidence.

Unavailable values remain nullable. Missing must never become zero. Each view model carries environment and quality/freshness. A single boolean isHealthy is insufficient.

## 5. Status and display rules

- HEALTHY, ATTENTION, CRITICAL, UNKNOWN, STALE and NOT_SUPPORTED are distinct.
- No successful observation means UNKNOWN, not healthy and not zero.
- An observation older than its configured freshness limit means STALE.
- Unsupported source/metric means NOT_SUPPORTED.
- Collector failure does not by itself prove the SAP target is down.
- Availability percentages require documented formula, denominator, window, source and missing-data treatment.
- Trend charts show gaps for missing/invalid data; never interpolate gaps into a healthy-looking line.
- LIVE alerts must be sourced events. Synthetic incidents are labelled DEMO.
- Overall state requires a documented aggregation policy; do not average component percentages without justification.
- Backup job success and tested recoverability are separate.
- Each KPI detail exposes definition, unit, source, observation time, freshness, threshold/rule version and evidence.

## 6. Widget-to-data binding

| Widget | Required input | Empty/unsupported behavior |
|---|---|---|
| DEV/QAS/PRD cards | Inventory, computed state, counts | “اطلاعات موجود نیست” + freshness |
| Overall status counts | Target states at a consistent snapshot time | Unknown is explicit |
| SAP/DB/filesystem/network rings | Approved metric and documented percentage formula | Unavailable state, no fabricated ring |
| Alert table | Normalized event records | Empty state; no fake LIVE incidents |
| CPU/memory/disk | Samples, unit and thresholds | Unavailable value + source/freshness |
| Response time | Defined operation, sample window and unit | Unavailable until definition approved |
| Work processes | Snapshot of configured total and state counts | Show numerator/denominator source and snapshot time |
| Database card | DB-specific approved adapter and definition | NOT_SUPPORTED if unconfirmed |
| Trend chart | Timestamped samples and quality flags | Show gaps and coverage |
| Environment matrix | System × domain state and freshness | Distinguish unknown/stale |
| Recent activity | Normalized events | No activity does not prove no issue |
| Quick links | Route registry and feature availability | Clear placeholder for incomplete feature |
| Header connection dot | Cockpit API/ingestion health | Keep separate from target health |
| Header clock | Browser/local time with timezone | Never imply it is SAP server time |

## 7. Machine implementation sequence

Execute in order. Each step produces a commit and passes its gate before the next starts.

### Step 0 — Repository/toolchain inventory
Inspect source tree, framework, package manager, lint/type/test commands and deployment target. Preserve existing code; do not scaffold a competing frontend before inventorying the repo.
Output: docs/implementation-inventory.md.
Gate: actual files and commands recorded; no assumed framework.

### Step 1 — Design tokens and shell
Implement CSS variables for navy surfaces, blue accent, spacing, radius, typography and semantic states. Set RTL and Persian font fallback. Build top bar, sidebar, hero and responsive grid. Use static skeleton/DEMO labels only.
Gate: reference hierarchy is recognizable on desktop; tablet/mobile usable; keyboard focus visible.

### Step 2 — Route registry
Create a typed route/feature registry for §3. Active navigation follows route; unknown routes get a safe not-found page. Incomplete sections show explicit placeholders.
Gate: every navigation item resolves; no dead controls.

### Step 3 — Canonical UI models
Implement view models and mapping functions from canonical records. Validate schema version and required fields at the boundary. Keep source-specific fields out of components.
Gate: tests cover mapping, missing/invalid values and unknown schema versions.

### Step 4 — DEMO data path
Use only synthetic fixtures explicitly marked DEMO. Show a persistent DEMO banner and environment badge in every view/export. Prevent environment mixing.
Gate: tests prove DEMO cannot be labelled LIVE.

### Step 5 — KPI cards and status summaries
Build reusable environment/status/access-domain cards. Centralize formatting, thresholds and state-to-color mapping. No metric card without approved definition/unit.
Gate: unknown, stale, unsupported and explicit zero are visually distinct.

### Step 6 — Alert table and evidence detail
Add sorting/filtering/pagination with bounded data and accessible actions. Event detail shows source, timestamps, target, sanitized evidence and quality. Never expose unrestricted dumps/job logs.
Gate: stable IDs and evidence references; sensitive fields masked.

### Step 7 — Performance cards and trends
Plot timestamped, unit-consistent series. Show range, unit, aggregation, source, gaps and freshness. Do not interpolate missing samples.
Gate: tests cover gaps, out-of-order points, mixed units and explicit zero.

### Step 8 — API client/backend
Use documented endpoints from docs/04-data-contract.md. Configure base URL outside source; enforce TLS/auth through approved deployment settings. Add timeout, cancellation, bounded retry and correlation IDs. Source/API failure becomes UNKNOWN/STALE, never healthy.
Gate: contract tests pass against a running backend; no secrets in browser bundle/Git.

### Step 9 — Environment matrix and activity
Bind counts to inventory and snapshot time. Build matrix/activity from normalized events and coverage. Show partial coverage and last-success time.
Gate: counts reconcile to source data; unknown coverage explicit.

### Step 10 — Security/audit UX
Enforce authorization server-side, not only by hiding controls. Add audit for configuration changes/exports where supported. Add redaction and bounded export.
Gate: unauthorized API access denied; privileged access/export auditable.

### Step 11 — Accessibility/localization QA
Verify RTL, keyboard navigation, focus order, screen-reader labels, contrast, zoom and narrow screens. Format Persian labels/dates consistently.
Gate: QA checklist and results recorded.

### Step 12 — Acceptance/release
Run unit, contract, integration, security, visual regression and resilience tests. Capture desktop/tablet/mobile screenshots and compare with reference. Record commit, environment, defects and sign-off.
Gate: blocking tests pass; limitations documented. No production-ready claim without live-source and security acceptance.

## 8. Suggested component responsibilities

Framework-equivalent names are acceptable if the existing repo uses another stack.

```text
App
├── AppShell
│   ├── TopBar
│   ├── SideNavigation
│   └── RouteOutlet
├── DashboardPage
│   ├── HeroHeader
│   ├── EnvironmentOverview
│   ├── OverallStatusSummary
│   ├── AccessDomainSummary
│   ├── ImportantEventsTable
│   ├── PerformanceGrid
│   ├── ResourceTrendChart
│   ├── QuickLinks
│   ├── EnvironmentHealthMatrix
│   └── RecentActivity
├── Shared
│   ├── StatusBadge
│   ├── FreshnessIndicator
│   ├── DemoBanner
│   ├── EmptyState
│   ├── EvidenceDrawer
│   └── ErrorState
└── Data
    ├── ApiClient
    ├── ContractValidator
    ├── ViewModelMappers
    ├── StatusRules
    └── Fixtures
```

## 9. Required automated tests

- Reject missing IDs/units, invalid timestamps and unknown environments.
- Explicit zero renders as zero; missing value renders unavailable.
- Stale/unknown never use healthy styling.
- DEMO label persists through navigation and export.
- Unsupported metric never renders fabricated value.
- Duplicate event IDs do not create duplicate rows; conflicting payloads surface diagnostics.
- Chart gaps remain gaps; mixed units are rejected or separated.
- Counts and matrix reconcile to fixtures/backend.
- API timeout, 401/403, 429, 5xx and malformed payload produce safe states.
- No credentials, raw sensitive logs or tokens in build artifacts.
- Keyboard navigation and responsive layouts tested.

## 10. Owner decisions still required

1. Exact frontend framework and existing app entry point.
2. Pixel-perfect screenshot reproduction vs composition/visual-language match.
3. Approved Persian labels for ambiguous navigation text.
4. Real environment names, counts, inventory and owners.
5. Formulas for availability rings, response time, work-process utilization and database percentage.
6. Thresholds, severity policy, freshness limits and aggregation rules.
7. Authentication/SSO, roles, RTL font and supported browsers.
8. Hosting/network topology and API base path.
9. Fixed 7/30-day chart ranges or user-selected range.
10. Whether screenshot values are illustrative. Default: DEMO only.

## 11. Definition of done

**UI-complete for DEMO:** all sections render responsively, controls work, labels are Persian/RTL, sample data is visibly DEMO and automated UI/contract tests pass.

**LIVE-pilot-ready:** every LIVE metric has confirmed source/version/authorization/units/freshness; source-to-UI tests pass on an approved representative system; polling load is accepted by the Basis owner; security sign-off is recorded.

A polished screenshot, hard-coded chart or synthetic fixture does not satisfy LIVE-pilot acceptance.
