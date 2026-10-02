---
id: agent-core-api
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: gRPC API Reference'
description: '**Contract source:** proto/novus.proto and proto/novus_runtime_surface.proto.
  Field numbers, message shapes, and service methods in those files are authoritative.
  This page is a...'
last_updated: '2026-10-02'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/API.md
managed_by: sync_private_docs
translation_status: pending
---
# NOVUS Agent-Core: gRPC API Reference

**Contract source:** `proto/novus.proto` and `proto/novus_runtime_surface.proto`. Field numbers, message shapes, and service methods in those files are authoritative. This page is a safe navigation reference, not a replacement for generated protobuf clients.

## Transport And Access

- Transport is gRPC over TLS.
- Normal privileged calls carry `x-request-timestamp`, `x-signature`, and `x-panel-uuid` metadata.
- The Agent applies its paired-Panel lock, request freshness, replay defense, rate limits, and audit policy before dispatching privileged calls.
- Pairing and standard gRPC health checks are bootstrap and liveness exceptions. Do not implement a client from this document alone; use the supported Panel transport or generated protobuf integration.

## NovusAgent

| Method | Interaction | Purpose |
| --- | --- | --- |
| `AgentTelemetry` | Unary | Collects host CPU, memory and disk telemetry. |
| `DockerManager` | Unary | Performs a permitted lifecycle action for a runtime container. |
| `PtyStream` | Bidirectional stream | Relays an authorized terminal session. |
| `RotateMasterSecret` | Unary | Rotates the paired Panel-to-Agent secret. |
| `PairNode` | Unary | Binds an unpaired Agent to one Panel using an approved pairing flow. |
| `UnclaimNode` | Unary | Removes the current Panel binding. |
| `UpdateAgent` | Unary | Requests the supported Agent update workflow. |

`PtyStream` frames use `open`, `input`, `resize`, `output`, `exit`, and `error` payloads. The initial client frame must open the session. Shell selection is constrained by Agent configuration; browsers never obtain direct host PTY access.

## InstanceService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateInstance` | Server stream | Provisions a game, service, or web runtime and streams progress. |
| `ReinstallInstance` | Server stream | Reinstalls an existing instance using current metadata and matrix defaults. |
| `CheckPorts` | Unary | Validates a candidate runtime port pool. |
| `AllocatePorts` | Unary | Atomically reserves an available port pool. |

## BackupService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateBackup` | Server stream | Creates an instance backup archive and streams progress. |
| `RestoreBackup` | Server stream | Restores a backup into an instance and streams progress. |
| `DeleteBackup` | Unary | Deletes a backup from the selected adapter. |
| `ListBackups` | Unary | Lists backup metadata for an instance. |

## NovusRuntimeSurface

| Area | Methods |
| --- | --- |
| Host and runtime inventory | `HostInfo`, `RuntimeContainers` |
| VFS | `VfsList`, `VfsStat`, `VfsRead`, `VfsWrite`, `VfsDelete`, `VfsChmod`, `VfsMove`, `VfsCopy`, `VfsMkdir`, `VfsCompress`, `VfsExtract`, `VfsUploadInit`, `VfsUploadChunk`, `VfsUploadFinalize` |
| Container lifecycle | `RuntimeContainerInspect`, `RuntimeContainerStats`, `RuntimeContainerCreate`, `RuntimeContainerRemove` |
| Container filesystem | `ContainerFsList`, `ContainerFsRead`, `ContainerFsWrite`, `ContainerFsMkdir`, `ContainerFsDelete`, `ContainerFsRename`, `ContainerFsPull` |
| Website certificate metadata | `WebsiteSslCertificates`, `WebsiteSslCertificate` |

`ContainerFsPull` is a server stream. The website methods expose certificate metadata; certificate issue and renewal are not methods of the current `NovusRuntimeSurface` contract.

## Compatibility Rules

- Additive protobuf fields and methods require coordinated Agent, Panel codec/client, tests, and release planning.
- Do not independently rename fields, change field numbers, alter metadata names, or change stream ordering.
- `NovusFileSystem` exists in `proto/novus_fs.proto`, but it is not a currently registered service surface. Do not use it as a supported runtime endpoint until registration and compatibility documentation are completed.

## Errors

Handlers use standard gRPC status codes. Clients must handle at least `InvalidArgument`, `Unauthenticated`, `PermissionDenied`, `FailedPrecondition`, `Unavailable`, `ResourceExhausted`, and `Internal`, and must display a user-safe message through the Panel rather than expose raw host details.
