# SRC Evidence Assessment — Phase 1

## Purpose and evidence boundary

This document records the evidence inventory visible under `SRC/` and the architecture implications for Phase 1. The folder contains SAP GUI captures/exports and reports; these are **environment evidence**, not proof that a corresponding interface is available or automatable. Binary PDFs, images and spreadsheets must be reviewed as evidence artifacts; filenames alone do not establish metric values, system release, or completeness.

## Evidence inventory observed

| Area | Artifacts visible in SRC | Intended use |
|---|---|---|
| Database backup / backup history | `DB12.pdf`, `DB12-01.png` through `DB12-11.png` | Understand visible backup screens, history and evidence limitations |
| CCMS monitoring | `RZ20.pdf` | Identify current monitoring tree and alert context |
| Workload | `ST03N.pdf`, `ST03N-01.pdf`, `ST03N-02.stats`, `ST03N-03.stats` | Inspect workload views and determine which measures are actually present |
| Operating system | `ST06.pdf`, `ST06-01.pdf` through `ST06-03.pdf` | Host metrics and OS monitoring integration clues |
| Work processes | `SM50.pdf`, `SM66.pdf` | Instance-local and system-wide work process state |
| Instances | `SM51.pdf` | Application server inventory and reported status |
| Background jobs | `SM37.pdf` | Job states and history; assess selection scope and timestamps |
| ABAP dumps | `ST22.pdf` | Dump counts, types and timestamps; avoid exposing sensitive dump payloads |
| System log | `SM21.pdf` | System events and errors with time window |
| Gateway | `SMGW.pdf` | Gateway status and connection evidence |
| Transport management | `STMS.pdf` | Transport domain/import history context; read-only in Phase 1 |
| Update requests | `SM13.pdf` | Update errors and backlog indicators |
| Locks / sessions | `SM12.xlsx`, `SM04.xlsx` | Lock/session evidence; validate columns, time scope and sensitivity |
| Other | `sapchart_dbg.txt`, `test.txt` | Treat as diagnostic/placeholder files until content and purpose are reviewed |

## Architecture decisions driven by this evidence

1. **Use source adapters, not transaction screen scraping.** SAP GUI transactions are useful for baseline and validation. They are not an acceptable production collection mechanism. Prefer SAP Host Agent interfaces, supported SAP interfaces, existing monitoring exports, or a tightly scoped custom ABAP read-only endpoint only after version/authorization checks.
2. **Separate inventory from health.** `SM51` establishes a view of instances at a point in time; it does not alone prove end-to-end system availability. Availability needs a defined probe and timestamp.
3. **Separate point-in-time status from trends.** `SM50/SM66` are snapshots; `ST03N` represents aggregated workload. Do not treat them as interchangeable or infer CPU saturation from workload alone.
4. **Use event windows and retention rules.** `SM37`, `ST22`, `SM21`, and `SM13` need explicit time windows, pagination/limits, severity mapping, and redaction. Avoid collecting full job logs or dump contents by default.
5. **Backup status is not recoverability.** `DB12` evidence may show backup-related state, but a successful backup record alone is not proof of a restorable backup. Recovery confidence requires catalog/backup-chain evidence and a documented restore test.
6. **Treat RZ20 as an input, not the only truth.** Existing CCMS alerts can supplement metrics; absence of an alert is not proof of health.
7. **Respect data minimization.** Session and lock data may include user names, transaction codes, object names or business identifiers. Store only fields required for operations; pseudonymize where feasible.
8. **Keep provenance.** Each observation must record source adapter, source object, collection time, observation time if available, quality, freshness, and any transformation/rule version.

## Source status

The files are registered as **EVIDENCE_PRESENT / CONTENT_REVIEW_PENDING** until their content has been parsed and values cross-checked. No source is marked API-CONFIRMED based only on a screenshot, PDF, or spreadsheet.

## Required next technical validation

- Identify SAP product/release, SAP_BASIS, kernel, database and OS for each SID/instance.
- Establish whether SAP Host Agent is installed and which supported interfaces are enabled.
- Verify each proposed metric against a real source and role with least privilege.
- Record the exact selection window, row count, timezone and export timestamp for each event report.
- Map field-level sensitivity and retention before ingestion.
- Confirm all DEV/QAS/PRD identifiers and avoid storing raw hostnames or IPs in the repository unless explicitly approved.
