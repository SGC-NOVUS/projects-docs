---
id: panel-core-manual-infrastructure-network
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Website Network Operations
description: The Websites workspace lets authorized operators manage supported website
  configuration, certificates and runtime actions through NOVUS-OS. The Panel authorizes
  each request and...
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/network.md
managed_by: sync_private_docs
---
# Website Network Operations

The Websites workspace lets authorized operators manage supported website
configuration, certificates and runtime actions through NOVUS-OS. The Panel
authorizes each request and the NOVUS Agent performs the node-local work.

## Operator Workflow

1. Select the managed website and confirm its node and domain.
2. Review configuration, certificate and runtime status in the Panel.
3. Use the provided actions to save a validated configuration, manage rewrite
   rules, request certificate work or schedule an approved runtime action.
4. Monitor the operation until it records success or a safe retry state.
5. Use the restore action only after verifying the target and requested
   confirmation value.

## Safety Model

- Website changes are permissioned, validated and audited.
- Configuration changes are checked before an active runtime reload.
- The Agent creates a recoverable revision before replacing managed
  configuration.
- Sensitive runtime actions use the established confirmation and asynchronous
  job workflow.

## Troubleshooting

Keep the job identifier, website and node when an action fails. Review the
operation result in the Panel and create an incident for repeated failures,
certificate errors or unavailable nodes. Do not alter host configuration or
service state outside the approved operational procedure.

Implementation details are restricted to the internal engineering procedure.
