---
id: panel-core-manual-resources-file-gateways
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: File Gateways
description: File Gateways define the approved storage mounts available to a managed
  runtime instance. Operators use the Panel to review and save gateway declarations;
  the runtime service en...
last_updated: '2026-10-02'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/resources/file_gateways.md
managed_by: sync_private_docs
translation_status: pending
---
# File Gateways

File Gateways define the approved storage mounts available to a managed runtime
instance. Operators use the Panel to review and save gateway declarations; the
runtime service enforces the resulting scope.

## Operator Workflow

1. Select the managed instance and review its gateway entries.
2. Choose an approved source and runtime destination presented by the Panel.
3. Select read-only or read-write access according to the workload need.
4. Save the declaration and review the returned validation result.
5. Use the permission-repair action only when the Panel reports that it is
   available and authorized.

## Safety Controls

- Gateway paths are restricted to the instance storage scope.
- Traversal, duplicate declarations and runtime-root mounts are rejected.
- Write and permission-repair actions require instance-write authority.
- Outcomes are recorded for audit and incident correlation.

## Failure Handling

Keep the instance identifier and validation error. Correct the declaration in
the Panel or escalate a repeated scope failure; do not create host mounts or
modify host permissions directly.

Mount resolution and runtime enforcement details are restricted to the internal
engineering procedure.
