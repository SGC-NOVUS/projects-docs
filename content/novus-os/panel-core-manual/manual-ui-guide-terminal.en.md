---
id: panel-core-manual-ui-guide-terminal
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Terminal
description: The Terminal workspace provides an authenticated, browser-native console
  for authorized operational work. It is a Panel surface, not a direct browser-to-host
  connection.
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/ui_guide/terminal.md
managed_by: sync_private_docs
---
# Terminal

The Terminal workspace provides an authenticated, browser-native console for
authorized operational work. It is a Panel surface, not a direct browser-to-host
connection.

## Operator Workflow

1. Open the Terminal workspace and select an approved session mode.
2. Connect only after confirming the target node and workload scope.
3. Use the session for authorized operational work and disconnect when finished.
4. Use the log viewer for approved diagnostic data rather than requesting raw
host log access.

## Safety Model

- Terminal and log operations require an authenticated Panel session and
  permission.
- Session lifecycle, terminal input and resize events use authenticated runtime
  transport.
- Log access is restricted to the approved scope; arbitrary host paths are not
  exposed.
- Connection and operation failures retain correlation data for the incident
  workflow.

## Troubleshooting

For an unavailable session, preserve the displayed error, target and timestamp.
Check node status through the Panel and use only a safe retry offered by the
workspace. Escalate persistent session or authorization failures.

Transport, daemon and compatibility details are restricted to the internal
engineering procedure.
