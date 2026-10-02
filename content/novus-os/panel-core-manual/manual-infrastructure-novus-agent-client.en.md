---
id: panel-core-manual-infrastructure-novus-agent-client
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: NOVUS Agent Transport
description: NOVUS Agent Transport is the Panel boundary for privileged node operations.
  It selects the registered node transport, applies Panel authorization and returns
  normalized results...
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/novus_agent_client.md
managed_by: sync_private_docs
---
# NOVUS Agent Transport

NOVUS Agent Transport is the Panel boundary for privileged node operations. It
selects the registered node transport, applies Panel authorization and returns
normalized results to Panel services. Operators do not connect to node runtime
services directly.

## Operator Expectations

- Register and pair nodes through the Panel workflow.
- Use the relevant Panel workspace for runtime, storage, backup, website and
  security actions.
- Review node health and operation status in the Panel before retrying work.
- Preserve correlation identifiers when escalating a failed node operation.

## Security Model

The Panel evaluates the operator policy before it submits intent to the Agent.
The Agent enforces its own node scope and authenticated transport boundary.
Credentials and registry access are never returned to browser clients or shown
in operator documentation.

## Related References

- [Node Management](nodes.md)
- [Platform Operations](../system/services.md)
- [gRPC Agent Contract](../../api-reference/grpc_agent_contract.md)

Driver, fallback and registry implementation details are restricted to the
internal engineering procedure.
