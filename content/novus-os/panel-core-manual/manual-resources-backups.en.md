---
id: panel-core-manual-resources-backups
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Backups
description: The Backups workspace protects website, database and managed instance
  data. Authorized operators use it to review recovery points, create protected snapshots,
  apply retention po...
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/resources/backups.md
managed_by: sync_private_docs
---
# Backups

The Backups workspace protects website, database and managed instance data.
Authorized operators use it to review recovery points, create protected
snapshots, apply retention policies and request a restore.

## Operator Workflow

1. Select the protected resource and review its latest successful recovery point.
2. Start a backup through the Panel and wait for its recorded completion state.
3. For a restore, verify the target resource and type the confirmation requested by the Panel.
4. Review the resulting audit event and validate the restored workload through its normal health checks.

## Plans And Retention

Backup plans define a protected source, schedule, retention period and optional offsite destination. Plan changes require backup-management permission. Review failed plans promptly and retain recovery points according to organizational policy.

## Safety Controls

- Backup actions are permissioned and audited.
- Restore and deletion require an explicit confirmation matched to the chosen resource.
- The Panel validates the selected source and restore target before it submits work to the managed runtime.
- Secrets used for database or offsite access are never shown in the UI or stored in backup metadata.

## When A Backup Fails

Keep the displayed job identifier, target and timestamp. Retry only after reviewing the failure in the Panel; escalate repeated failures or a missing recovery point to the platform response team. Do not inspect or modify backup storage directly.

Implementation, retention execution and protected recovery procedures are
restricted to the internal engineering procedure.
