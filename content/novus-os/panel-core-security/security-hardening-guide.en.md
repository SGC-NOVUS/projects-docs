---
id: panel-core-security-hardening-guide
cluster: novus-os
category: panel-core-security
order: 100
status: active
version: 0.1.0
title: Platform Security Operations
description: This guide is for authorized NOVUS-OS operators. Use the Security workspace
  in the Panel for firewall rules, access reviews, security status and recovery requests.
  Host-level co...
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/security/hardening_guide.md
managed_by: sync_private_docs
---
# Platform Security Operations

This guide is for authorized NOVUS-OS operators. Use the Security workspace in
the Panel for firewall rules, access reviews, security status and recovery
requests. Host-level configuration is performed only by the approved engineering
procedure.

## Security Posture

NOVUS-OS combines permissioned Panel workflows, authenticated Agent transport,
encrypted secrets, multi-factor controls and audit records. The platform keeps
security configuration outside tenant workloads and applies least-privilege
access to each operation.

## Operator Workflow

1. Review alerts, audit events and node status in the Security workspace.
2. Confirm the target scope before changing a firewall rule or responding to an
   access event.
3. Use a required confirmation or multi-factor prompt for sensitive actions.
4. Record the change through the organization's change-control process.
5. Escalate configuration drift, suspected credential exposure and unavailable
   security services to the authorized response team.

## Incident Response

When an abnormal security signal appears, preserve its Panel audit identifiers,
timestamps and affected resources. Stop only workflows for which the Panel
offers a safe cancellation action. Do not alter host services, credentials or
filesystem state directly; the response team follows the protected recovery
procedure.

## Operational Checks

- Access is assigned to individual accounts and reviewed regularly.
- Sensitive actions require the permissions and confirmation expected by the
  Panel.
- Nodes are paired and managed through approved Panel workflows.
- Backup and recovery readiness is reviewed through the relevant Panel modules.
- Production changes have an accountable change record.

## Related Guides

- [System Security](../manual/system/security.md)
- [Permission Guard](../manual/system/permission_guard.md)
- [Users And Access](../manual/system/users.md)
- [Backups](../manual/resources/backups.md)

Detailed host hardening, privileged configuration and recovery procedures are
restricted to the internal engineering procedure.

Internal implementation documentation is excluded from the public documentation build.
