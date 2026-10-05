---
id: novus-os-control-plane-runtime-contract
cluster: novus-os
category: architecture
order: 10
status: active
version: 0.1.0
title: Control-Plane and Runtime Contract
description: Responsibilities, transport boundaries, service surfaces, and failure behavior between panel-core and novus-agent.
last_updated: 2026-10-05
source_locale: en
locale: en
---
# Control-Plane and Runtime Contract

## Responsibility Boundary

`panel-core` owns user-facing workflows, authorization, and control-plane state. It sends typed operations to `novus-agent`; it is not the component that performs the agent's host and runtime work. The agent composes the Docker and VFS services and exposes the supported operations through its gRPC server.

This boundary has three consequences:

1. A panel action is not successful merely because its HTTP request passed panel validation. The runtime call must also complete and report its result.
2. Privileged runtime behavior belongs to the agent implementation and its typed contract, not to browser code or an arbitrary shell endpoint.
3. A change that alters request fields or behavior must update the matching Protobuf contract and the public documentation together.

## Transport and Request Identity

The agent listens for gRPC on `NOVUS_AGENT_GRPC_LISTEN`, defaulting to `:9443`. The server uses TLS credentials. The panel's direct driver creates a TLS channel using the configured CA certificate and may set an expected server name. The current code does **not** configure client-certificate authentication, so this transport must not be described as mutual TLS (mTLS).

For authenticated calls, the panel sends `x-request-timestamp`, `x-signature`, and `x-panel-uuid` metadata. The signature is HMAC-SHA256 over the encoded Protobuf request followed by the timestamp; the agent compares the expected signature in constant time. Timestamps outside the configured clock-skew window are rejected; the default window is 15 seconds. A replay guard rejects a signature already seen within that window.

After pairing, the agent checks that the request's panel UUID matches its bound panel identity. The default rate limit is 600 requests per minute with a burst of 120. These controls apply to unary and streaming RPCs through server interceptors.

## Registered Runtime Services

The daemon registers these application services:

| Service | Responsibility |
| --- | --- |
| `NovusAgent` | Agent telemetry, Docker operations, PTY streaming, node pairing state, secret rotation, and agent update operations. |
| `NovusRuntimeSurface` | Host information, VFS operations, container lifecycle and filesystem operations, and website SSL metadata. |
| `InstanceService` | Instance creation/reinstallation progress and port checks/allocation. |
| `BackupService` | Backup creation, restoration, deletion, listing, and streaming progress. |

The daemon also registers the standard gRPC health service. The authoritative request and response fields are the `.proto` files; this summary does not replace those wire contracts.

## Timeouts and Failure Behavior

The panel direct driver uses a 10-second default gRPC timeout unless a call or node configuration provides another value. A transport timeout or unavailable agent is an operation failure, not a successful empty response. The caller must surface the failure and may retry only when the operation is safe to repeat; the protocol does not make every mutating call idempotent by default.

The agent cannot start its gRPC runtime if it cannot load persistent state, TLS credentials, or bind the configured listener. During a request, missing authentication metadata, an invalid or expired timestamp, a bad/replayed signature, or a panel-binding violation is rejected before the service handler runs. Handler errors are returned to the caller and recorded by the audit logger when audit logging is enabled.

## Contract Maintenance

When adding or changing an RPC:

- Update the Protobuf request/response definition and regenerate the language bindings.
- Register the implementation in the daemon runtime.
- Update the panel direct driver and its timeout/streaming behavior.
- Add coverage for both the successful operation and its rejection/failure path.
- Update this document and the relevant API or operations guide in the same change.

Related contracts: `proto/novus.proto`, `proto/novus_runtime_surface.proto`, `internal/grpcserver/daemon_runtime.go`, and the panel `NovusAgentDirectDriver`.
