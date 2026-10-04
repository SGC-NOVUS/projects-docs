---
id: panel-core-manual-system-scheduler
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Scheduler
description: The Scheduler workspace manages approved recurring jobs for Panel-owned
  operations. Jobs execute through the platform scheduler and remain subject to permissions,
  audit records...
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/system/scheduler.md
managed_by: sync_private_docs
---
# Scheduler

The Scheduler workspace manages approved recurring jobs for Panel-owned
operations. Jobs execute through the platform scheduler and remain subject to
permissions, audit records and resource scope.

## Operator Workflow

1. Review active jobs and their most recent result.
2. Create or edit a job using the Panel schedule form.
3. Confirm the target resource and permitted action.
4. Observe the execution history and investigate failed runs.
5. Disable a job before making a material production change.

## Safety Controls

- Schedule expressions and job payloads are validated before saving.
- Jobs cannot grant broader authority than the initiating policy allows.
- Execution history preserves timing, outcome and correlation information.
- Host scheduling configuration is an internal platform responsibility.
