---
id: panel-core-manual-system-services
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Platform Operations
description: The Platform Operations workspace gives authorized operators a single
  control surface for managed services, node health, scheduled work and operational
  alerts. Host administrati...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/system/services.md
managed_by: sync_private_docs
---
# Platform Operations

The Platform Operations workspace gives authorized operators a single control surface for managed services, node health, scheduled work and operational alerts. Host administration remains behind the authenticated NOVUS Agent and approved response procedures.

## Operator Workflow

1. Review current health, alerts and queued work in the Panel.
2. Select the affected managed service or node.
3. Use the available Panel action and complete its confirmation requirements.
4. Observe the operation state until it completes or reports a safe retry.
5. Record the action and outcome through the organization change process.

## Boundaries

- The Panel evaluates operator permissions and presents results.
- The NOVUS Agent performs approved host-local work through typed transport.
- Operators do not use direct host shells, service managers or local runtime control paths for routine Panel operations.
- Audit records preserve the initiating identity, target and outcome.

## Escalation

If a service is unavailable or a requested action cannot complete, retain the Panel correlation identifier, timestamps and affected resource. Use the incident workflow for production impact. Do not bypass the Panel or alter host configuration directly.

Internal service ownership, compatibility boundaries and recovery procedures are
restricted to the engineering workspace.
