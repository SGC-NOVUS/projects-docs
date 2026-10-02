---
id: agent-core-vfs
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: NOVUS Agent-Core - Virtual File System (VFS)
description: VFS in agent-core is a host-side filesystem abstraction used by NovusRuntimeSurface
  RPC handlers. It enforces path validation and symlink hardening before file operations
  are ex...
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/VFS.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core - Virtual File System (VFS)

## 1. Overview

VFS in agent-core is a host-side filesystem abstraction used by
`NovusRuntimeSurface` RPC handlers. It enforces path validation and symlink
hardening before file operations are executed.

## 2. Current Runtime Scope

The `pkg/vfs` service supports allowlist roots via `Config.AllowedRoots`.

Current runtime bootstrap behavior:
- runtime composition resolves roots through policy mode (`pkg/vfs/policy.go`) and then initializes `pkg/vfs` with resolved allowlist.
- `NOVUS_AGENT_VFS_POLICY_MODE=host_admin` resolves host-wide root (`/`).
- `NOVUS_AGENT_VFS_POLICY_MODE=scoped_runtime` resolves scoped runtime roots (default `/var/lib/novus/volumes/games`, `/var/lib/novus/volumes/service`, `/var/lib/novus/volumes/web`, or `NOVUS_AGENT_VFS_SCOPED_ROOTS` override).

## 3. Path Validation Model

`resolvePath()` in `pkg/vfs/service.go` enforces:
- `filepath.Clean()` normalization.
- absolute path requirement.
- null-byte rejection.
- lexical root containment check against configured allowlist.
- symlink-hardening via `resolveRealPath()`:
  - resolve symlinks on the deepest existing ancestor,
  - rebuild unresolved suffix,
  - re-check containment after symlink resolution.

If validation fails, the operation is rejected.

## 4. Implemented Operations

Read surface:
- `VfsList`, `VfsStat`, `VfsRead`.

Write/mutation surface:
- `VfsWrite`, `VfsMkdir`, `VfsChmod`, `VfsDelete`, `VfsMove`, `VfsCopy`.

Archive surface:
- `VfsCompress`, `VfsExtract`.

Upload/download surface:
- `VfsUploadInit`, `VfsUploadChunk`, `VfsUploadFinalize`.
- `VfsDownloadInit`, `VfsDownloadChunk` (service-level API).

## 5. Upload Sessions (actual implementation)

Chunked upload is implemented in-memory (no Redis dependency in current agent-core):
- session store: in-process map guarded by mutex.
- default session TTL: 2 hours (`sessionTTL` in `pkg/vfs/service.go`).
- sequential chunk enforcement (`upload_sequence_out_of_order` on violations).
- optional checksum verification on finalize.
- size verification when total size is provided.
- atomic move to final path using `os.Rename()` after successful finalize.

## 6. Runtime Directories

From `internal/config/config.go` and `pkg/vfs/service.go`:
- upload work directory defaults to `/var/lib/novus/uploads`.
- archive/work directory defaults to `/var/lib/novus/work`.

Both are created on startup if missing.

## 7. Known Gaps and Roadmap Alignment

Current documented and tracked gaps:
- host-admin remains the default mode for compatibility unless operators switch to `scoped_runtime`.
- granular path ACL layers (AllowedSubpaths, HiddenPaths/MaskedPaths, operation flags) are still tracked as follow-up hardening.

These gaps are tracked in:
- `docs/architecture/FULL_MODULAR_MASTER_PLAN_AGENT.md`
- `docs/dev/AGENT_ENTERPRISE_MASTER_PLAN_2026-09-24.md`
