---
id: novus-os-grpc-mtls-boundary
cluster: novus-os
category: security
order: 20
status: active
version: 0.1.0
title: gRPC mTLS and Signature Boundary
description: Security boundary for gRPC metadata signature, clock skew policy, and
  replay protection.
last_updated: 2026-10-01
source_locale: en
locale: ru
translation_status: pending
---
# gRPC mTLS and Signature Boundary

## Security Controls
- gRPC channel is protected with TLS credentials.
- Metadata must include timestamp and signature.
- Requests outside allowed skew are denied.
- Signature replay attempts are denied.

## Operational Policy
- All new runtime methods must be governed by contract-first protobuf updates.
- Any security policy change must be reflected in docs and changelog within the same release.
