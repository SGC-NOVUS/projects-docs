---
id: panel-core-getting-started-readme
cluster: novus-os
category: panel-core-getting-started
order: 100
status: active
version: 0.1.0
title: Getting Started With NOVUS-OS Panel
description: NOVUS-OS Panel is the Control-Plane of the platform. It provides the
  browser workspace for users and operators while delegating privileged host work
  to the authenticated NOVUS A...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/getting-started/README.md
managed_by: sync_private_docs
---
# Getting Started With NOVUS-OS Panel

NOVUS-OS Panel is the Control-Plane of the platform. It provides the browser workspace for users and operators while delegating privileged host work to the authenticated NOVUS Agent.

## First Session

1. Open the approved Panel URL supplied by your administrator.
2. Sign in with the account issued to you and complete any required multi-factor verification.
3. Start from **Dashboard** to review accessible nodes, services, alerts and operational tasks.
4. Open a feature module only when your assigned permissions allow the workflow.

## Common Workflows

| Goal | Guide |
| --- | --- |
| Review services and instances | [Infrastructure: Instances](../manual/infrastructure/instances.md) |
| Work with managed files | [Infrastructure: VFS](../manual/infrastructure/vfs.md) |
| Review backups | [Resources: Backups](../manual/resources/backups.md) |
| Manage websites and network resources | [Infrastructure: Network](../manual/infrastructure/network.md) |
| Use terminal access | [UI Guide: Terminal](../manual/ui_guide/terminal.md) |
| Understand permissions and security | [System: Permission Guard](../manual/system/permission_guard.md) |

## Safety Boundaries

The Panel is not a direct root shell. Host, runtime, filesystem and terminal operations are authorized by the Panel and performed through the Agent transport. Do not attempt to replace product workflows with browser-side commands, copied tokens, or direct host access.

For developers, begin with [Architecture Overview](../dev/architecture_overview.md). For API integrations, use the checked contract in [OpenAPI 3.1](../api-reference/openapi_3.1.yaml).
