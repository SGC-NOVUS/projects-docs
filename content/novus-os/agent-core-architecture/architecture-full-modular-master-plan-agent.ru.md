---
id: agent-core-architecture-full-modular-master-plan-agent
cluster: novus-os
category: agent-core-architecture
order: 100
status: active
version: 0.1.0
title: ПОЛНЫЙ МОДУЛЬНЫЙ ГЕНПЛАН — AGENT CORE (КАНОНИЧЕСКИЙ SSoT)
description: 'Статус: ЗАВЕРШЕН И ЗАБЛОКИРОВАН (Базовая версия v0.2.0, 2026-09-25)'
last_updated: '2026-10-02'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/architecture/FULL_MODULAR_MASTER_PLAN_AGENT.md
managed_by: sync_private_docs
---
# FULL MODULAR MASTER PLAN - AGENT CORE (CANONICAL SSoT)

Status: COMPLETED & LOCKED (Baseline v0.2.0, 2026-09-25)

Scope: agent-core only, with cross-repository boundary compliance to panel-core and installer.

Normative anchors:
- AGENTS.md
- ECOSYSTEM_MANIFEST.md

This file supersedes operational split planning as the authoritative master plan.
Working artifacts in docs/dev remain supporting records, not a parallel source of truth.

## 0. Mission, Scope, and Non-Negotiable Constraints

Mission:
- Evolve agent-core into an enterprise-grade, modular, security-first Go runtime
  while preserving platform compatibility and transport contracts.

Non-negotiable constraints:
- No breaking gRPC contract drift during migration.
- Security controls remain enforced end-to-end (TLS, signed metadata, replay, rate limit, audit).
- No business capability loss for telemetry, runtime operations, VFS, backup, PTY, WebSocket console, SSH/SFTP.
- Deterministic phase gates with reproducible validation.
- Installer and Panel interoperability preserved across releases.

## 0.1 Current Execution Snapshot (2026-09-25)

Execution status:
- Overall completion: 100.0% (35/35 checkpoints).
- Phase A (Contract Freeze and Reconciliation): 100% complete.
- Phase B (Composition Root and Module Skeleton): 100% complete.
- Phase C (Transport/Domain Separation): 100% complete.
- Phase D (Security Hardening): 100% complete.
- Phase E (Compatibility and Deprecation Bridge): 100% complete.
- Phase F (Legacy Cleanup and Wrapper Removal): 100% complete.
- Phase G (Release Readiness and Operational Proof): 100% complete.

Baseline metrics:
- Go package count: 14.
- Go source file count: 55.
- Test files: 16.
- Current hotspots:
  - pkg/vfs/service.go (~748 LOC)
  - internal/grpcserver/vfs_surface.go (~742 LOC)
  - internal/grpcserver/runtime_surface_service.go (~610 LOC)
  - pkg/docker/service.go (~601 LOC)
  - internal/grpcserver/instance_service.go (~596 LOC)
  - internal/grpcserver/backup_service.go (~592 LOC)
  - internal/grpcserver/service.go (~556 LOC)

Validation baseline (latest run):
- go test ./... -count=1: green
- go vet ./...: green
- go build ./...: green

## 1. Authoritative Product and Contract Invariants

## 1.1 API Surface and Contract Drift Resolution

Authoritative decision:
- BackupService and ReinstallInstance remain official platform gRPC contract surface.

Required invariant:
- Contract source in proto/novus.proto, generated stubs, and runtime registration are treated as an indivisible baseline.

Enforcement:
- Contract drift guard test is mandatory in CI and local gates.
- Any service/method addition or removal requires coordinated source contract, generated code, handlers, tests, docs, and release sequencing.

## 1.2 Transport Hardening Invariants (WebSocket and SSH)

Authoritative decision:
- WebSocket and SSH remain enabled by default.

Mandatory hardening requirements:
- WebSocket:
  - Remove wildcard CheckOrigin behavior.
  - Enforce strict JWT claim validation bound to node, container, and session context.
- SSH/SFTP:
  - Host key must be persistent and generated once.
  - Persist key under secure host state path (/etc/novus-agent/ or state path policy aligned with NOVUS_AGENT_STATE_FILE lifecycle).
  - Remove hardcoded :2022 from runtime bootstrap and move to configuration.
  - Route SFTP disk access through a unified VFS Policy Engine.
  - Require filepath.EvalSymlinks canonicalization before all effective filesystem operations.

## 1.3 VFS Architecture Invariant: Context-Aware OIM/IAM Policy Engine

The VFS architecture must evolve from binary scope selection to granular policy processing.

Mandatory policy modes:
- host_admin mode:
  - Full host filesystem access for trusted node-administration workflows.
- scoped_runtime mode:
  - Baseline tenant/runtime isolation to /var/lib/novus/volumes/* roots.

Mandatory granular OIM/IAM path-level guard capabilities:
- AllowedSubpaths:
  - Positive allowlist of concrete subtrees inside runtime volumes.
- HiddenPaths and MaskedPaths:
  - Deny visibility in directory listings and metadata responses for protected paths.
- AccessFlags:
  - Path-level operation flags: Read, Write, Delete, Chmod.
- Symlink-Traverse Guard:
  - Canonicalize via filepath.EvalSymlinks, then evaluate final target against policy masks and flags.

Boundary invariant:
- Agent enforces technical scope and path guard execution; Panel remains IAM/OIM decision authority.

## 1.4 Binary Update Pipeline Invariant (P0)

Mandatory behavior:
- Full removal of script-based update execution (curl | bash prohibited).
- Update pipeline must be binary-driven:
  - fetch release metadata via GitHub Releases API,
  - download Linux ELF artifact,
  - verify required SHA-256 checksum,
  - perform atomic binary swap via os.Rename,
  - restart unit under controlled policy with rollback path on failed activation.

## 2. Full Audit Report (Consolidated)

## 2.1 Critical Findings

1) Unsafe updater execution path.
- Evidence: internal/grpcserver/service.go (UpdateAgent path invoking shell script pipeline).
- Risk: supply-chain/RCE exposure.

2) Historical contract drift risk (now reconciled in source contract and docs, guard retained).
- Evidence context: runtime registration vs source proto divergence prior to reconciliation.
- Risk: panel/agent incompatibility and non-reproducible protobuf generation.

3) WebSocket origin and claim hardening gap.
- Evidence: wildcard origin acceptance and insufficient context binding.
- Risk: cross-origin/token misuse in compatibility transport.

## 2.2 High Findings

1) SFTP path enforcement bypasses unified VFS policy path.
- Evidence: direct os.* operations in SFTP adapter path.
- Risk: inconsistent containment behavior and symlink traversal exposure.

2) Runtime VFS scope defaults to host-wide root.
- Evidence: bootstrap AllowedRoots set to /.
- Risk: scoped tenant isolation not yet enforced by default runtime policy mode.

3) SSH host identity lifecycle and configurability debt.
- Evidence: non-persistent host key lifecycle and hardcoded SSH port in bootstrap path.
- Risk: identity instability and reduced operational governance.

## 2.3 Medium Findings

1) Dead or weakly integrated paths.
- Command handler and scheduler orchestration integration require explicit ownership and lifecycle cleanup.

2) Documentation drift (partially remediated).
- Config keys and behavior claims must continuously track runtime reality.

3) Coverage density mismatch for high-risk surfaces.
- Transport and security-heavy paths require deeper focused tests.

## 3. Target Modular Architecture

## 3.1 Domain Model

Target domains:
- BootstrapCLI
- ConfigRuntime
- StateVault
- SecurityGateway
- RuntimeSurface
- InstanceLifecycle
- BackupOrchestration
- FilesVFS
- ContainerRuntime
- TransportWebSocketConsole
- TransportSSHSFTP
- UpdateManager
- SchedulerJobs
- Observability

## 3.2 Module Layout Standard

For each domain D:
- internal/modules/D/application
- internal/modules/D/domain
- internal/modules/D/infrastructure
- internal/modules/D/transport
- internal/modules/D/providers

Platform layer:
- internal/platform/bootstrap
- internal/platform/config
- internal/platform/observability
- internal/platform/contracts

Boundary rules:
- No cross-domain imports into another domain infrastructure package.
- Domain collaboration only via explicit ports/interfaces.
- Transport adapters remain thin; orchestration belongs to application layer.

## 4. Documentation Governance Standard (Strict)

Documentation must evolve in lockstep with architecture and implementation.

Mandatory documentation contours:

1) Developer contour (docs/development/):
- module internals, extension of gRPC surfaces, type contracts,
  panel-agent protocol behavior, test standards, fitness controls.

2) Operator and system administrator contour (docs/ public operator set):
- environment configuration, exposed ports, systemd settings,
  SSH/TLS persistence model, security posture, network isolation, diagnostics.

3) User/reference contour (docs/ public reference set):
- environment variable references, VFS limits/capabilities,
  SFTP and web console functional references.

4) Internal engineering contour (docs/dev/):
- private audits, debt ledgers, execution trackers, migration notes.

Security sanitization requirement:
- Public docs must remain deeply functional but enforce zero disclosure of exploit chains,
  private host secret paths, bypass guidance, or offensive operational details.

## 5. Sequential Phase Plan (A -> G)

## Phase A. Contract Freeze and Reconciliation (Completed)

Delivered outcomes:
- Source contract reconciliation for BackupService and ReinstallInstance.
- API reference alignment.
- Contract drift guard introduced.
- Gate checks green.

## Phase B. Composition Root and Module Skeleton (Completed)

Delivered outcomes:
- internal/platform/bootstrap introduced.
- internal/modules skeleton introduced.
- remaining daemon startup wiring extracted from internal/grpcserver/server.go
  into internal/platform/bootstrap while preserving listener and lifecycle parity.
- startup parity smoke and full gates green.
- Phase B sign-off complete.

Gate B:
- all Gate A checks
- startup smoke parity for gRPC, WS, SSH listeners
- no behavior drift in grpc_smoke_test

## Phase C. Transport/Domain Separation

- C1 delivered:
  - NovusAgent application service introduced under internal/modules/novusagent/application.
  - gRPC transport delegates telemetry, docker manager, pairing, unclaim, and rotate-secret orchestration to module service.
  - Focused module unit tests added for extracted orchestration paths.
- C2 delivered:
  - RuntimeSurface application service introduced under internal/modules/runtime_surface/application.
  - RuntimeSurface HostInfo, RuntimeContainers, RuntimeContainerInspect, RuntimeContainerStats, RuntimeContainerRemove, and RuntimeContainerCreate orchestration moved out of grpc transport into module application service.
  - gRPC RuntimeSurface transport now acts as decode/encode/status envelope for these paths.
  - Focused module unit tests added for extracted RuntimeSurface orchestration paths.
- C3 delivered:
  - InstanceLifecycle application service introduced under internal/modules/instance_lifecycle/application.
  - CheckPorts, AllocatePorts, CreateInstance, and ReinstallInstance orchestration moved out of grpc transport into module application service.
  - gRPC InstanceService transport now delegates these paths while preserving response/status contracts and streaming envelopes.
  - Focused module unit tests expanded for extracted InstanceLifecycle orchestration paths.
  - BackupOrchestration application service introduced under internal/modules/backup_orchestration/application.
  - CreateBackup, RestoreBackup, DeleteBackup, and ListBackups orchestration moved out of grpc transport into module application service.
  - gRPC BackupService transport now delegates these paths while preserving stream envelopes and status mappings.
  - Focused module unit tests added for extracted BackupOrchestration paths.
- C4 delivered:
  - WebSocket console orchestration moved into `internal/modules/transport_websocket_console/application/service.go`.
  - gRPC compatibility transport `internal/grpcserver/websocket_console.go` now acts as HTTP/WebSocket adapter and delegates auth/buffer/spam/control mapping to module application service.
  - Focused module unit tests added for websocket auth, ring buffer, spam throttling, and client control mapping.
- C5 delivered:
  - Phase C sign-off completed after green full quality gates (`go test ./...`, `go vet ./...`, `go build ./...`).
- Split NovusAgent, RuntimeSurface, InstanceLifecycle, BackupOrchestration into module services.
- Keep transport handlers as decode/encode/validation envelopes.
- Split websocket console into transport adapter plus application service.

## Phase D. Security Hardening Implementation

- D1 delivered:
  - Script-based updater path removed from `internal/grpcserver/service.go`.
  - Binary update manager module introduced in `internal/modules/update_manager/application/service.go`.
  - `UpdateAgent` now delegates asynchronous binary update flow to module application service.
  - Focused unit tests added for update manager binary download and activation flow.
- D2 delivered:
  - Mandatory SHA-256 verification introduced for updater artifacts via `checksums.txt` release metadata.
  - Binary activation now proceeds only after expected checksum and downloaded checksum match.
  - Focused unit tests added for checksum download failure, missing checksum entry, and checksum mismatch paths.
- D3 delivered:
  - Explicit rollback strategy implemented for updater activation and restart failure paths.
  - Failed restart now triggers binary rollback to the previous executable and a restart attempt with restored binary.
  - Focused unit tests added for restart-failure rollback behavior.
- D4 delivered:
  - SSH host key lifecycle now persists key material to a secure host path aligned with state-file policy.
  - Runtime bootstrap removed hardcoded SSH listener and now uses configuration-driven listener address.
  - Focused unit tests added for host key create/reuse/permissions and corrupted-key rejection behavior.
- D5 delivered:
  - FilesVFS policy resolver introduced with explicit `host_admin` and `scoped_runtime` modes.
  - Bootstrap and legacy runtime wiring now resolve VFS allowlist roots from policy mode instead of hardcoded host-wide root.
  - Focused unit tests added for policy-mode resolution, scoped-root validation, and config defaults/overrides.
- D6 delivered:
  - WebSocket transport removed wildcard origin behavior and now enforces explicit origin allowlist policy.
  - JWT authentication now validates contextual claims for node, container, and session binding.
  - Focused unit tests added for origin policy checks and strict claim-validation paths.
- D7 delivered:
  - Phase D sign-off completed with fresh hardening gate evidence.
  - Full validation rerun successful: `go test ./... -count=1`, `go vet ./...`, `go build ./...`.
  - Security-hardening sequence D1-D6 confirmed complete without regressions.
- Implement binary updater manager with mandatory SHA-256 and atomic swap/rollback.
- Implement persistent SSH host key lifecycle and configurable SSH listener address.
- Implement FilesVFS policy resolver with host_admin and scoped_runtime modes.
- Implement granular OIM/IAM path ACL guard:
  - AllowedSubpaths
  - HiddenPaths and MaskedPaths
  - AccessFlags
  - Symlink canonicalization and policy enforcement before operation dispatch.
- Harden WebSocket origin and JWT context binding.

## Phase E. Compatibility and Deprecation Bridge

- E1 delivered:
  - Configuration compatibility aliases implemented for documented runtime-drift keys.
  - Legacy `NOVUS_AGENT_STATE_PATH` now maps to canonical `NOVUS_AGENT_STATE_FILE` when canonical key is not set.
  - Legacy `NOVUS_AGENT_VFS_ALLOWED_ROOTS` now maps to scoped roots and preserves scoped-runtime behavior when explicit mode is absent.
- E2 delivered:
  - Runtime deprecation warnings added for legacy alias usage (`NOVUS_AGENT_STATE_PATH`, `NOVUS_AGENT_VFS_ALLOWED_ROOTS`).
  - Canonical key precedence preserved while emitting startup warnings when alias values are the active source.
- E3 delivered:
  - Operator docs aligned to canonical config keys with explicit legacy-alias migration guidance.
  - Configuration reference now documents canonical precedence and startup warning semantics for deprecated aliases.
- E4 delivered:
  - Phase E sign-off completed after fresh full quality gate rerun.
  - Validation evidence: `go test ./... -count=1`, `go vet ./...`, `go build ./...` all green.
- Preserve legacy config aliases where needed.
- Introduce deprecation warnings and canonical key migration path.
- Align docs and runtime key references.

## Phase F. Legacy Cleanup and Wrapper Removal

- F1 delivered:
  - Transitional startup wrapper `grpcserver.Run` removed from `internal/grpcserver/server.go`.
  - gRPC smoke test switched to canonical daemon lifecycle (`NewDaemon` + scheduler + compatibility transport startup + `Serve`) without wrapper path.
  - Fresh full quality gates rerun after wrapper removal remained green.
- F2 delivered:
  - Dead adapter `internal/grpcserver/command_handler.go` removed after confirming zero runtime/test call-sites.
  - Full quality gate rerun after dead-code removal remained green.
- F3 delivered:
  - Transport adapters further thinned by removing stale legacy helper/state code from `internal/grpcserver/backup_service.go` and `internal/grpcserver/instance_service.go`.
  - Daemon wiring updated to use reduced constructor signatures in `internal/grpcserver/daemon_runtime.go`.
- F4 delivered:
  - Phase F sign-off completed after fresh full quality gate rerun.
  - Validation evidence: `go test ./... -count=1`, `go vet ./...`, `go build ./...` all green.
- Remove transitional wrappers once module ownership is complete.
- Remove dead adapters and enforce module-boundary rules.

## Phase G. Release Readiness and Operational Proof

- G1 delivered:
  - Production-like updater proof executed via focused module tests:
    - `TestUpdateSwapsExecutableWithDownloadedBinary`
    - `TestUpdateRollsBackOnRestartFailure`
  - Evidence confirms download+checksum+activation path and rollback behavior on restart failure.
- G2 delivered:
  - Transport resilience and compatibility sequencing validated via fresh test run:
    - `go test ./internal/grpcserver ./internal/sshserver -count=1 -v`
  - Evidence includes contract drift guard, gRPC smoke flow, WebSocket origin/context checks, and SSH host-key lifecycle coverage.
- G3 delivered:
  - Final release sign-off completed after fresh full quality gate rerun.
  - Validation evidence: `go test ./... -count=1`, `go vet ./...`, `go build ./...` all green.
- Execute production-like update/restart/rollback proof.
- Validate transport resilience and compatibility sequencing.
- Sign off release checklist.

## 6. Progress Model and Tracking

Progress formula:
- completion_percent = (completed_checkpoints / total_checkpoints) * 100

Current:
- Total checkpoints: 35
- Completed checkpoints: 35
- Completion: 100.0%

Checkpoint ledger:

Phase A checkpoints (7):
- [x] A1 inventory and baseline report captured
- [x] A2 source proto reconciled with runtime/generated backup and reinstall surface
- [x] A3 API docs updated for contract surface
- [x] A4 gate checks passed
- [x] A5 contract drift guard introduced
- [x] A6 architecture/docs parity delta reduced
- [x] A7 Phase A sign-off

Phase B checkpoints (5):
- [x] B1 bootstrap package introduced
- [x] B2 module skeleton introduced
- [x] B3 remaining server wiring extraction completed
- [x] B4 startup parity verified
- [x] B5 Phase B sign-off

Phase C checkpoints (5):
- [x] C1 NovusAgent split
- [x] C2 RuntimeSurface split
- [x] C3 Instance and Backup split
- [x] C4 WebSocket adapter split
- [x] C5 Phase C sign-off

Phase D checkpoints (7):
- [x] D1 script updater path removed
- [x] D2 SHA-256 mandatory
- [x] D3 atomic swap and rollback strategy
- [x] D4 SSH host key persistence
- [x] D5 VFS policy modes implemented
- [x] D6 WebSocket hardening completed
- [x] D7 Phase D sign-off

Phase E checkpoints (4):
- [x] E1 config compatibility aliases
- [x] E2 deprecation warnings
- [x] E3 docs aligned with canonical keys
- [x] E4 Phase E sign-off

Phase F checkpoints (4):
- [x] F1 wrapper removal
- [x] F2 dead code removal
- [x] F3 module boundary enforcement
- [x] F4 Phase F sign-off

Phase G checkpoints (3):
- [x] G1 update and rollback proof
- [x] G2 transport resilience proof
- [x] G3 final release sign-off

## 7. Continuous Evolution: The Anti-Monolithic Modular Invariant
Все последующие доработки ядра агента подчиняются правилу нулевой монолитной экспансии (Zero-Monolith Policy):   
1) Запрет на расширение общих и корневых слоев: Запрещено добавлять бизнес-логику в internal/grpcserver, main.go, общие хелперы или платформенные пакеты internal/platform/*.   
2) Маршрутизация функционала (Domain Routing):
  -Существующий домен: Если задача относится к существующей функциональности (InstanceLifecycle, RuntimeSurface, FilesVFS, UpdateManager и т.д.), реализация ведётся исключительно внутри соответствующего модуля (internal/modules/<Domain>/...).
  -Новый домен: Если задача представляет новый независимый контекст (например, HypervisorKVM, MetricsEngine, TelemetryUDP), она оформляется строго как новый автономный модуль по каноническому стандарту (application, domain, infrastructure, transport).   
3) Слабая связанность (Loose Coupling): Межмодульное взаимодействие разрешено только через публичные интерфейсы портов, шину событий или типизированные контракты без циклических и инфраструктурных импортов.  

## 8. Completion Definition

Program completion requires all checkpoints closed and all below true:
- runtime services decomposed to planned module boundaries,
- no critical unresolved gap in updater, VFS policy engine, or SSH host identity,
- gRPC/API compatibility preserved for Panel and Installer integrations,
- legacy orchestration reduced to thin transport shims,
- documentation synchronized to runtime behavior for all required audiences,
- all quality and release readiness gates green.
