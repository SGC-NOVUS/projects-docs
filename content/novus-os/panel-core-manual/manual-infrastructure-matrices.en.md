---
id: panel-core-manual-infrastructure-matrices
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Runtime Matrices
description: Runtime Matrices define approved workload templates, resource expectations,
  network declarations and managed storage requirements. Operators choose a matrix
  through the Panel wh...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/matrices.md
managed_by: sync_private_docs
---
# Runtime Matrices

Runtime Matrices define approved workload templates, resource expectations,
network declarations and managed storage requirements. Operators choose a matrix
through the Panel when creating or updating an instance.

## Operator Workflow

1. Select the workload category and supported matrix.
2. Review the exposed resource, network and storage summary.
3. Apply approved overrides through the Panel form.
4. Confirm the resulting plan before provisioning.
5. Observe the job result and preserve its identifier for incident handling.

## Safety Controls

- Matrix data is validated before provisioning.
- Storage and network declarations are scoped to the managed instance.
- Unsupported image, volume or port changes are rejected by the runtime policy.
- Provisioning outcomes are audited and correlated with the instance.

Matrix authoring and runtime mapping details are restricted to the internal
engineering workspace.
