---
id: panel-core-manual-system-security
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: System Security
description: NOVUS-OS applies layered security controls across identity, permissions,
  browser sessions, the Control-Plane, the Agent transport and managed workloads.
  This guide is for author...
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/system/security.md
managed_by: sync_private_docs
---
# System Security

NOVUS-OS applies layered security controls across identity, permissions, browser sessions, the Control-Plane, the Agent transport and managed workloads. This guide is for authorized operators using the Panel; it is not a host-hardening command reference.

## Security Responsibilities

| Area | Operator responsibility |
| --- | --- |
| Identity | Use an individual account, multi-factor verification where required, and the least privileged role for each task. |
| Access | Review user, team and API access regularly; remove access that is no longer required. |
| Nodes | Pair and manage nodes only through the approved Panel workflow. |
| Workloads | Use Panel workflows for runtime, file, network and backup operations rather than direct host access. |
| Incidents | Preserve relevant Panel audit evidence and follow the approved incident-response process. |

## Secure Operations

- Review alerts and security status in the Panel before making privileged changes.
- Use the required confirmation or multi-factor flow for sensitive operations.
- Keep browser sessions, API credentials, integration tokens and recovery material private.
- Verify an action's target node, instance and scope before confirming it.
- Record production changes through the organization's change-control process.

## When Something Looks Wrong

1. Stop the affected workflow if the Panel provides a safe cancellation path.
2. Do not attempt direct host remediation or bypass an authorization requirement.
3. Preserve the relevant Panel status, audit identifiers and timestamps for the authorized response team.
4. Escalate suspected credential exposure, unauthorized access or integrity failures through the private security process.

## Related Guides

- [Permission Guard](permission_guard.md)
- [Users And Access](users.md)
- [Settings](settings.md)
- [Node Management](../infrastructure/nodes.md)
- [Getting Started](../../getting-started/README.md)

Detailed host hardening and implementation-level remediation are restricted to
the internal engineering procedure.
