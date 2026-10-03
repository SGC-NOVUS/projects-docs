---
id: panel-core-architecture-frontend-bundle-budget-report
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: Frontend Bundle Budget Report
description: 'Overall status: PASS Dashboard status: FAIL'
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/frontend_bundle_budget_report.md
managed_by: sync_private_docs
---
# Frontend Bundle Budget Report

Overall status: PASS
Dashboard status: FAIL

## Sources

- Manifest: /tmp/novus-panel-build/manifest.json
- Baseline: tools/quality/frontend_bundle_budget_baseline.json
- History: docs/architecture/frontend_bundle_budget_history.json
- Headroom percent: 10
- History snapshots: 8

## Global Metrics

| Metric | Current | Cap | Usage | Status |
|---|---:|---:|---:|---|
| totalJsBytes | 3.98 MiB (4169148) | 5.16 MiB (5410377) | 77.1% | PASS |
| totalCssBytes | 337.02 KiB (345107) | 359.33 KiB (367955) | 93.8% | PASS |
| largestJsBytes | 893.07 KiB (914508) | 896.59 KiB (918109) | 99.6% | PASS |

## Entry JS Budgets

| Metric | Current | Cap | Usage | Status |
|---|---:|---:|---:|---|
| entryJs:resources/js/app.js | 99.29 KiB (101675) | 104.50 KiB (107011) | 95.0% | PASS |
| entryJs:resources/js/setup.js | 51.18 KiB (52412) | 52.88 KiB (54150) | 96.8% | PASS |

## Entry CSS Budgets

| Metric | Current | Cap | Usage | Status |
|---|---:|---:|---:|---|
| entryCss:resources/js/app.js | 327.86 KiB (335729) | 348.57 KiB (356931) | 94.1% | PASS |
| entryCss:resources/js/setup.js | 313.30 KiB (320819) | 332.55 KiB (340530) | 94.2% | PASS |

## Budget Headroom Dashboard

| Metric | Current | Cap | Usage | Remaining Headroom | Risk |
|---|---:|---:|---:|---:|---|
| largestJsBytes | 893.07 KiB (914508) | 896.59 KiB (918109) | 99.6% | +3.52 KiB (+3601) | CRITICAL |
| entryJs:resources/js/setup.js | 51.18 KiB (52412) | 52.88 KiB (54150) | 96.8% | +1.70 KiB (+1738) | WATCH |
| entryJs:resources/js/app.js | 99.29 KiB (101675) | 104.50 KiB (107011) | 95.0% | +5.21 KiB (+5336) | WATCH |
| entryCss:resources/js/setup.js | 313.30 KiB (320819) | 332.55 KiB (340530) | 94.2% | +19.25 KiB (+19711) | WATCH |
| entryCss:resources/js/app.js | 327.86 KiB (335729) | 348.57 KiB (356931) | 94.1% | +20.71 KiB (+21202) | WATCH |
| totalCssBytes | 337.02 KiB (345107) | 359.33 KiB (367955) | 93.8% | +22.31 KiB (+22848) | WATCH |
| totalJsBytes | 3.98 MiB (4169148) | 5.16 MiB (5410377) | 77.1% | +1.18 MiB (+1241229) | OK |

- Usage risk thresholds: WATCH >= 92% · CRITICAL >= 98%
- Metrics at WATCH/CRITICAL: 6
- Metrics with invalid caps: 0

## Growth Signals (Latest Snapshot Delta)

- Current snapshot commit: 45dee3385fb1
- Previous snapshot commit: 58ca53a5af1c
| Metric | Previous | Current | Delta | Delta % | Warn Threshold | Fail Threshold | Signal |
|---|---:|---:|---:|---:|---:|---:|---|
| totalJsBytes | 4.73 MiB (4956212) | 3.98 MiB (4169148) | -787064 B (-787064) | -15.88% | 3% | 8% | OK |
| totalCssBytes | 329.79 KiB (337706) | 337.02 KiB (345107) | +7.23 KiB (+7401) | +2.19% | 3% | 8% | OK |
| largestJsBytes | 815.45 KiB (835021) | 893.07 KiB (914508) | +77.62 KiB (+79487) | +9.52% | 3% | 8% | FAIL |

- Growth thresholds: WARN > 3% · FAIL > 8%
- Growth warnings/failures: 1

## Top 12 JS Assets

| # | Asset | Size |
|---:|---|---:|
| 1 | assets/module-scheduler-CZur5sqe.js | 893.07 KiB (914508) |
| 2 | assets/module-overview-mLB4L4ac.js | 493.69 KiB (505538) |
| 3 | assets/module-bots-1oNhRVRo.js | 410.38 KiB (420229) |
| 4 | assets/route-terminal-COvZnTO6.js | 384.14 KiB (393364) |
| 5 | assets/module-services-ui-BTqkrwWW.js | 257.48 KiB (263656) |
| 6 | assets/module-services-overlays-rX1BL-bO.js | 189.08 KiB (193618) |
| 7 | assets/module-services-detail-tabs-CLG5LMCN.js | 126.85 KiB (129899) |
| 8 | assets/module-matrices-CsV0k3rV.js | 124.09 KiB (127073) |
| 9 | assets/module-websites-Bp8IJbaF.js | 122.24 KiB (125174) |
| 10 | assets/module-profile-DmMj6HaN.js | 117.77 KiB (120593) |
| 11 | assets/module-files-Dj_-xuZ0.js | 105.26 KiB (107783) |
| 12 | assets/app-CaNKTWnY.js | 99.29 KiB (101675) |

## Trend Snapshots (Last 8)

| # | Commit | Total JS | Delta JS | Total CSS | Delta CSS | Largest JS | Status |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | 1726cef4eec0 | 2.58 MiB (2704317) | n/a | 240.76 KiB (246542) | n/a | 494.98 KiB (506855) | PASS |
| 2 | f01486c22ccb | 3.18 MiB (3338940) | +619.75 KiB (23.5%) | 245.21 KiB (251095) | +4.45 KiB (1.8%) | 1.03 MiB (1078608) | FAIL |
| 3 | f01486c22ccb | 2.64 MiB (2766950) | -571990 B (-17.1%) | 245.21 KiB (251095) | 0 B (0.0%) | 495.54 KiB (507429) | PASS |
| 4 | f01486c22ccb | 2.64 MiB (2770403) | +3.37 KiB (0.1%) | 244.71 KiB (250588) | -507 B (-0.2%) | 495.54 KiB (507429) | PASS |
| 5 | 5b9552e22176 | 4.69 MiB (4918524) | +2.05 MiB (77.5%) | 326.66 KiB (334504) | +81.95 KiB (33.5%) | 815.08 KiB (834644) | PASS |
| 6 | e9982488c9c8 | 4.71 MiB (4940170) | +21.14 KiB (0.4%) | 326.66 KiB (334504) | 0 B (0.0%) | 815.32 KiB (834885) | PASS |
| 7 | 58ca53a5af1c | 4.73 MiB (4956212) | +15.67 KiB (0.3%) | 329.79 KiB (337706) | +3.13 KiB (1.0%) | 815.45 KiB (835021) | PASS |
| 8 | 45dee3385fb1 | 3.98 MiB (4169148) | -787064 B (-15.9%) | 337.02 KiB (345107) | +7.23 KiB (2.2%) | 893.07 KiB (914508) | PASS |

## Gate Outcome

- Budget metrics are within configured caps.
- Dashboard has active warnings/failures; see Budget Headroom Dashboard and Growth Signals sections.

## Refresh Commands

```bash
npm run --silent build:ci
node tools/quality/frontend_bundle_budget_check.mjs
node tools/quality/frontend_bundle_budget_history_update.mjs
node tools/quality/frontend_bundle_budget_report.mjs
```
