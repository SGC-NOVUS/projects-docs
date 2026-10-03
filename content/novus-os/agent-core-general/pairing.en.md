---
id: agent-core-pairing
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Pairing'
description: Pairing establishes a single trusted Panel binding for an Agent. After
  successful pairing, privileged runtime calls are accepted only from the bound Panel
  through the signed gRP...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/PAIRING.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core: Pairing

Pairing establishes a single trusted Panel binding for an Agent. After successful pairing, privileged runtime calls are accepted only from the bound Panel through the signed gRPC transport.

## Supported Flow

1. An operator generates a one-time pairing token on an unpaired Agent using the supported CLI workflow.
2. The Panel submits `PairNodeRequest` with its UUID, the one-time token, and a securely provisioned master secret.
3. The Agent validates that it is unpaired, validates the Panel UUID and token, persists the binding, and returns pairing status with Agent and Panel identities.
4. Subsequent privileged calls use the normal signed transport and must match the bound Panel identity.

The token is one-time and expires according to `NOVUS_AGENT_PAIRING_TOKEN_TTL_MINUTES`. Never paste pairing tokens or master secrets into tickets, public documentation, shell history, or source control.

## Contract Summary

| RPC | Required request intent | Result |
| --- | --- | --- |
| `PairNode` | Request UUID, Panel UUID, pairing token, master secret, optional Panel name | Establishes the initial Panel binding. |
| `UnclaimNode` | Request UUID, bound Panel UUID, optional reason | Removes the current binding after normal transport authorization. |
| `RotateMasterSecret` | Request UUID, bound Panel UUID, optional old-secret fingerprint, replacement secret | Replaces the secret for the current binding. |

The exact field definitions and numbers are in `proto/novus.proto`. The Agent does not return the master secret in `PairNodeResponse`.

## Single-Panel Boundary

The Agent retains one bound Panel UUID. Requests from another Panel are denied. Pairing cannot overwrite an existing binding; operators must use the approved unclaim/recovery workflow first.

## Operator Guidance

- Pair the Agent only through the Panel node-registration workflow or an approved recovery procedure.
- Verify the node identity in the Panel before approving pairing.
- Treat unclaim and secret rotation as security-sensitive administration actions.
- For connection errors, inspect the Agent service status and Panel node health; do not disable transport verification to diagnose a problem.
