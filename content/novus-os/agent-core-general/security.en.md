---
id: agent-core-security
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent: Security Model'
description: NOVUS Agent is the host-side Data-Plane daemon. It accepts only the supported
  Panel transport and is not a general-purpose administrative endpoint.
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/SECURITY.md
managed_by: sync_private_docs
---
# NOVUS Agent: Security Model

NOVUS Agent is the host-side Data-Plane daemon. It accepts only the supported Panel transport and is not a general-purpose administrative endpoint.

## Trust Boundaries

- gRPC transport requires TLS.
- Privileged requests are authenticated with the paired Panel identity, a signed request, freshness validation, replay protection, and per-identity rate limiting.
- After pairing, the Agent is bound to one Panel. A request from a different Panel identity is denied.
- Pairing, unclaim and secret rotation are security-sensitive control-plane operations and must be initiated through the approved Panel workflow.

The signing implementation, timing policy, secret material and state-storage details are internal security information. Use the supported Panel client or generated contract tooling rather than implementing an ad-hoc client.

## Host Execution

The Agent performs permitted container, filesystem, telemetry and terminal operations only after transport validation. Terminal sessions use an approved shell policy and are relayed through the Panel; browsers do not receive direct host-shell access.

Filesystem operations normalize requested paths and apply symlink hardening. Context-specific runtime VFS policies remain an active hardening area; operators must not assume tenant isolation beyond the currently supported workflow and assigned Panel permissions.

## Audit And Operations

When audit logging is enabled, the Agent emits structured request-security lifecycle events for operational review. Treat audit records as sensitive: they may contain method names, reasons and Panel identifiers.

Operators should:

1. Deploy the Agent only through the approved release and installation path.
2. Restrict network exposure according to the approved infrastructure policy.
3. Monitor Agent availability and authentication failures through the Panel and host observability system.
4. Rotate pairing credentials through the supported control-plane flow.
5. Keep secrets, TLS material, pairing tokens and host logs out of source control and public support channels.

For supported settings, see [Configuration Reference](CONFIGURATION.md). Internal
implementation findings are restricted to the engineering workspace.
