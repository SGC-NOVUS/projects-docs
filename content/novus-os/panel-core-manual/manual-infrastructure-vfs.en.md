---
id: panel-core-manual-infrastructure-vfs
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Files And Storage
description: The Files workspace provides permissioned access to managed instance
  and site storage through the NOVUS Agent. The Panel authorizes every request; it
  does not grant browser clie...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/vfs.md
managed_by: sync_private_docs
---
# Files And Storage

The Files workspace provides permissioned access to managed instance and site storage through the NOVUS Agent. The Panel authorizes every request; it does not grant browser clients direct access to host filesystems.

## Operator Workflow

1. Select the intended node and managed resource.
2. Browse only the storage presented by the workspace.
3. Use Panel actions to upload, edit, move, archive or download files.
4. Confirm deletion and other destructive actions using the value requested by the Panel.
5. Review the completed operation in the audit trail before continuing.

## Available Actions

- Browse file and directory metadata.
- Download or edit authorized files.
- Upload large files through a resumable transfer.
- Create directories, move or copy items, and manage permissions when the role allows it.
- Create or extract supported archives within the selected managed scope.

## Security Model

- The Panel validates paths and permissions before requesting Agent work.
- The Agent independently restricts operations to the resource scope it owns.
- Destructive operations require explicit confirmation and are audited.
- Transfers are scoped to an authenticated operation; the browser never receives host-level filesystem authority.

## Troubleshooting

If a file action fails, keep the operation identifier and selected resource. Check the node status in the Panel, then retry only when the workspace reports a safe retry path. Escalate unavailable nodes, repeated authorization failures or suspected path-scope issues to the platform team.

Transport, local compatibility and recovery implementation details are restricted
to the internal engineering procedure.
