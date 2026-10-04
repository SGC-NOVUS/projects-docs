---
id: panel-core-manual-system-permission-guard
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Permission Guard
description: Permission Guard is the NOVUS Panel security posture surface. It helps
  authorized operators review whether the Panel environment meets the platform's expected
  access and configu...
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/system/permission_guard.md
managed_by: sync_private_docs
---
# Permission Guard

Permission Guard is the NOVUS Panel security posture surface. It helps authorized operators review whether the Panel environment meets the platform's expected access and configuration boundaries.

## What It Protects

- The separation between the Panel application, managed tenant workloads and host-level secrets.
- Access to security-sensitive product workflows through roles, permissions and multi-factor requirements.
- Detection of configuration states that require operator attention before privileged features are used.

Permission Guard does not grant additional access and does not replace the NOVUS Agent. Host-level operations remain authorized by the Panel and performed through the Agent or approved installation workflow.

## Operator Workflow

1. Sign in with an account that has the required security administration permission.
2. Open the Security area of the Panel and review the current posture and reported findings.
3. Resolve findings through the approved Panel workflow or the controlled operations process.
4. Re-run the security review after an authorized configuration change.
5. Record production changes through your normal change-control process.

## Access Model

Security actions are permission-gated. Operators should use the least privileged role required for the task and must not share accounts, multi-factor factors, API credentials or elevated sessions.

If a security action is unavailable, request the required role through the organization's access-management process. Do not bypass the Panel, modify host permissions manually, or copy privileged commands from internal engineering documentation.

## Related Guides

- [System Security](security.md)
- [Settings](settings.md)
- [Users And Access](users.md)
- [Getting Started](../../getting-started/README.md)

Implementation-level checks, host paths and remediation mechanisms are restricted to `docs/dev/PERMISSION_GUARD_IMPLEMENTATION.md` for authorized engineering work.
