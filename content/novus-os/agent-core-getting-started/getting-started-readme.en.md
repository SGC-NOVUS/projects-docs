---
id: agent-core-getting-started-readme
cluster: novus-os
category: agent-core-getting-started
order: 100
status: active
version: 0.1.0
title: Getting Started With NOVUS Agent
description: NOVUS Agent is the host-side Data-Plane service for NOVUS-OS. It executes
  authorized runtime operations and exposes the typed transport used by the Panel;
  it is not a user-facin...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/getting-started/README.md
managed_by: sync_private_docs
---
# Getting Started With NOVUS Agent

NOVUS Agent is the host-side Data-Plane service for NOVUS-OS. It executes authorized runtime operations and exposes the typed transport used by the Panel; it is not a user-facing web application.

## Recommended Path

1. Install the Agent through the approved NOVUS Installer or approved release procedure.
2. Confirm the service is healthy using the deployment runbook.
3. Pair the Agent through the Panel node-registration workflow.
4. Manage instances, files, telemetry and terminals through the Panel according to assigned permissions.

## Next Guides

| Goal | Guide |
| --- | --- |
| Deploy or operate the service | [Deployment](../DEPLOYMENT.md) |
| Configure supported settings | [Configuration Reference](../CONFIGURATION.md) |
| Pair a node safely | [Pairing](../PAIRING.md) |
| Understand RPC compatibility | [gRPC API Reference](../API.md) |
| Review transport guarantees | [Security](../SECURITY.md) |

Do not expose the Agent directly as a general-purpose administration endpoint. Keep all credentials, pairing data and host secrets in approved secret-management paths.
