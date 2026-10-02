---
id: panel-core-manual-ui-guide-dashboard
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Dashboard
description: The Dashboard provides an operational overview of managed nodes, workloads,
  alerts, tasks and platform health. It is a read-oriented workspace with approved
  actions for authoriz...
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/ui_guide/dashboard.md
managed_by: sync_private_docs
---
# Dashboard

The Dashboard provides an operational overview of managed nodes, workloads,
alerts, tasks and platform health. It is a read-oriented workspace with approved
actions for authorized operators.

## Operator Workflow

1. Review current health, capacity and alert summaries.
2. Select a resource to open its dedicated management workspace.
3. Use a displayed action only after confirming its target and required scope.
4. Track task progress and preserve correlation identifiers for failed work.
5. Create or update an incident when a failure affects production service.

## Safety Model

- Dashboard data is collected through authenticated runtime services.
- Actions remain permissioned and are audited by the owning domain.
- The Dashboard never grants direct host, runtime socket or filesystem access.
- Deployment and asset maintenance remain internal platform procedures.
