---
id: panel-core-manual-resources-databases
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Databases
description: The Databases workspace manages user-created data-plane databases and
  presents read-only inventory from connected nodes. Control-plane data is isolated
  from tenant database oper...
last_updated: '2026-10-02'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/resources/databases.md
managed_by: sync_private_docs
translation_status: pending
---
# Databases

The Databases workspace manages user-created data-plane databases and presents read-only inventory from connected nodes. Control-plane data is isolated from tenant database operations.

## Operator Workflow

1. Select the node and database scope in the Panel.
2. Review databases, tables, users and grants before requesting a change.
3. Use the provided forms to create a database, manage users or adjust grants.
4. Confirm destructive actions only after verifying the selected resource.
5. Use the Backups workspace to create a recovery point before a destructive change or an export.

## Access Model

- Database administration requires the database-management permission.
- Exports require the dedicated backup-export permission.
- Connected nodes support distributed inventory. Write operations are available only where the current node contract explicitly allows them.
- System control-plane stores are not exposed as tenant database targets.

## Safe Operations

The Panel validates names, scopes and grants before forwarding a request to the database owner. Credentials are not returned in API responses or displayed after creation. Use least privilege, rotate credentials through the approved workflow and record production changes through change control.

## Recovery And Escalation

For failed operations, preserve the Panel request identifier and error state. Do not run direct database commands or change schemas outside an approved maintenance procedure. Recoveries and schema diagnostics are handled by the authorized platform team.

Implementation, topology and migration procedures are restricted to the internal
engineering procedure.
