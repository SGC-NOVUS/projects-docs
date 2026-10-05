---
id: novus-os-grpc-mtls-boundary
cluster: novus-os
category: security
order: 20
status: active
version: 0.1.0
title: gRPC TLS and HMAC Signature Boundary
description: TLS transport and request-authentication behavior implemented between panel-core and novus-agent.
last_updated: 2026-10-05
source_locale: en
locale: en
---
# gRPC TLS and HMAC Signature Boundary

## Transport Is TLS, Not mTLS

The agent's gRPC server loads a server certificate and private key and serves the channel over TLS. The panel's direct driver supplies a configured CA certificate and can set a server-name override. The current client channel does not present a client certificate, and the agent does not configure a client-certificate verification policy. Therefore, the implemented transport is TLS with application-level request authentication, not mutual TLS.

If the configured certificate or key is missing, the agent attempts to create a self-signed certificate in its configured TLS directory. Operators must ensure that the panel trusts the certificate authority and uses the expected server name for that node.

## Signed Request Metadata

Authenticated unary and streaming calls carry:

| Metadata | Meaning |
| --- | --- |
| `x-request-timestamp` | Unix timestamp in seconds used for freshness validation. |
| `x-signature` | Hexadecimal HMAC-SHA256 signature for the encoded Protobuf request and timestamp. |
| `x-panel-uuid` | Panel identity checked against the agent's pairing state. |

The agent rejects missing metadata, malformed timestamps, and timestamps outside the allowed clock-skew window. The default window is 15 seconds. Signature comparison is constant-time. The replay guard rejects a signature previously observed inside the active time window.

## Rejection and Audit Behavior

Authentication failures are returned as gRPC `UNAUTHENTICATED`; a panel identity that violates the paired-panel lock is rejected as `PERMISSION_DENIED`. Requests over the configured per-panel rate limit are rejected as `RESOURCE_EXHAUSTED`. The defaults are 600 requests per minute and a burst of 120.

When audit logging is enabled, rejected calls and handler outcomes are written as structured events. Do not put master secrets, private keys, or complete credential material in application logs or documentation.

## Operational Policy

- Keep request fields and service methods contract-first in the Protobuf definitions.
- Rotate pairing credentials only through the supported panel workflow.
- Update the transport description, operational guidance, and changelog whenever the implemented authentication behavior changes.

Implementation references: `internal/grpcserver/server.go`, `internal/grpcserver/daemon_runtime.go`, `internal/security/interceptors.go`, and the panel `NovusAgentDirectDriver`.
