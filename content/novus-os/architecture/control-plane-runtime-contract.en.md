---
id: novus-os-control-plane-runtime-contract
cluster: novus-os
category: architecture
order: 10
status: active
version: 0.1.0
title: Control-Plane and Runtime Contract
description: Canonical contract between panel-core Control-Plane and novus-agent Data-Plane.
last_updated: 2026-10-01
source_locale: en
locale: en
---
# Control-Plane and Runtime Contract

## Scope
This document defines the operational boundary between panel-core and novus-agent.

## Key Rules
- panel-core does not execute privileged host operations directly.
- novus-agent is the execution boundary for privileged runtime actions.
- Transport-level authentication and replay protection are mandatory.

## Contract Surfaces
- gRPC runtime services for typed operations.
- OpenAPI control endpoints for panel workflows.
- Shared audit and changelog governance for change traceability.
