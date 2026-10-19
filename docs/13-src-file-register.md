# SRC File Register

Source directory: [SRC](../SRC)

The following inventory is based on filenames exposed by the repository directory. It is a navigation and review register, not a claim that all content has been semantically validated.

## Transaction evidence

| Artifact | Topic | Review question |
|---|---|---|
| `SM51.pdf` | Application server list | Which SIDs/instances are shown and what is their timestamp? |
| `SM50.pdf`, `SM66.pdf` | Work processes | Which states and durations are visible? Is the view a snapshot? |
| `ST06.pdf`, `ST06-01.pdf`–`ST06-03.pdf` | OS monitoring | Which metrics are populated, with what units and host context? |
| `ST03N.pdf`, `ST03N-01.pdf`, `ST03N-02.stats`, `ST03N-03.stats` | Workload | What period, workload type, and aggregation do the exports represent? |
| `SM37.pdf` | Background jobs | Which job statuses/time range are included? Are job names/users sensitive? |
| `ST22.pdf` | ABAP dumps | Are entries summarized, and can payloads expose application data? |
| `SM21.pdf` | System log | What is the period, severity and message coverage? |
| `SM13.pdf` | Update requests | Are failed updates and their age represented? |
| `SM12.xlsx` | Locks | Which columns exist and which should be redacted? |
| `SM04.xlsx` | User sessions | Which fields are necessary for operational monitoring? |
| `RZ20.pdf` | CCMS alerts | Is there an exportable supported interface or only GUI evidence? |
| `DB12.pdf`, `DB12-01.png`–`DB12-11.png` | Backup evidence | Does the material show catalog state, backup completion, or restore validation? |
| `STMS.pdf` | Transport system | Which read-only status/history can be exposed safely? |
| `SMGW.pdf` | Gateway | What state and connection data are shown? |
| `sapchart_dbg.txt`, `test.txt` | Miscellaneous | Confirm purpose before use; do not treat as production evidence |

## Evidence review checklist

- [ ] File content reviewed (not just filename)
- [ ] System / SID / environment identified or safely pseudonymized
- [ ] Capture/export timestamp and timezone recorded
- [ ] Selection window and filters recorded
- [ ] Metric definition and units verified
- [ ] Sensitive fields identified and redaction applied
- [ ] Candidate source interface mapped
- [ ] Coverage status assigned
- [ ] Validation owner and follow-up action recorded

## Important limitation

A PDF or screenshot of a transaction proves only that a screen/report was captured. It does not prove the underlying data can be collected by a supported API, at the required polling interval, or with least-privilege authorization. Keep these distinctions explicit in the source coverage matrix.
