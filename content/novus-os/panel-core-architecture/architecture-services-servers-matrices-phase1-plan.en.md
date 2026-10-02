---
id: panel-core-architecture-services-servers-matrices-phase1-plan
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: NOVUS-OS Services/Servers/Matrices Overhaul — Phase 1 Plan
description: Act as the Principal Enterprise Architect and Lead UI/UX Engineer. Acknowledge
  this directive, read the panel-main reference, and provide a step-by-step technical
  plan for Phase...
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/services_servers_matrices_phase1_plan.md
managed_by: sync_private_docs
---
# NOVUS-OS Services/Servers/Matrices Overhaul — Phase 1 Plan

## Directive (as requested)

Act as the Principal Enterprise Architect and Lead UI/UX Engineer. Acknowledge this directive, read the panel-main reference, and provide a step-by-step technical plan for Phase 1. Begin implementation immediately after the plan.

## Acknowledgment

Directive accepted. This Phase 1 plan is grounded in:
- panel-main domain behavior (node viability, allocation selection, variable governance, and server creation orchestration)
- current panel-novus runtime topology (instance-centric model, network channel pool, profile tables)
- current agent-core envelope limits (partial CPU/RAM cgroups only)

## Architectural Pivot (2026-05-22)

Pre-Phase 1 pivot accepted and applied:
1. Node registry moved from flat-file-first behavior to DB-first behavior in `panel_nodes`.
2. Canonical allocation storage moved to `panel_node_allocations` linked to `panel_nodes.id`.
3. Legacy JSON state files remain as compatibility fallback/import source during transition.

## Non-Negotiable Constraints

1. No direct code copy from panel-main.
2. Preserve public APIs used by current panel-novus frontend and agents.
3. Introduce canonical schema and services with backward-compatible fallback paths.
4. Enforce hard resource checks where capacity is explicitly configured.

## panel-main Logic Reconstructed (Mathematical/Architectural)

1. Node viability formula:
- effective_limit = base_capacity * (1 + overallocate_pct / 100)
- viable(resource) = (current_committed + requested) <= effective_limit

2. Allocation selection policy:
- find free IP:port candidates on a target node
- dedicated mode excludes addresses already consumed by other bindings
- deterministic first-available selection can replace random choice for reproducibility

3. Provisioning pipeline shape:
- resolve viable node
- resolve allocation(s)
- validate variables/rules
- persist server/instance
- dispatch runtime creation

4. Variable governance:
- reserved environment keys are blocked
- dynamic validation rules are enforced before commit

## Phase 1 Scope (This Wave)

1. Canonical node pool model in novus_os.
2. Canonical allocations table and allocator service.
3. Hard-deny resource ledger checks on create/resources-write paths.
4. Strict runtime limits envelope propagation into container create payload.
5. Proto expansion in agent-core (additive, backward-compatible).

## Step-by-Step Technical Plan

1. Schema foundation:
- add idempotent migration to create/patch `panel_nodes`
- add idempotent migration to create/patch `allocations`
- backfill `panel_nodes` from observed node_agent_id in runtime tables
- backfill `allocations` from `panel_network_channels` for transition continuity

2. Domain services:
- add `NodeResourceLedgerService` to compute used/free/limit with overallocate math
- add `AllocationPoolService` for first-available IP:port reservation from `allocations`

3. Pipeline wiring:
- enforce ledger checks in `InstanceMutationService::create()`
- enforce ledger checks in `InstanceProfileService::saveResources()` with self-exclusion
- update `ProvisioningService` to prefer `allocations` pool and fallback to legacy `panel_network_channels` when canonical pool is not active

4. Strict limits transport:
- extend provisioning payload with disk/swap/oom/pids fields
- extend agent-core docker create request/host config mapping to enforce cgroups/storage/pids where supported

5. Contract expansion:
- add additive `ContainerHardwareLimits` message in `agent-core/proto/novus.proto`
- attach optional limits envelope in `DockerManagerRequest` (no breaking RPC changes)
- regenerate `internal/gen/novus/v1/*.pb.go`

6. Verification:
- panel-novus targeted unit test updates (payload builder)
- syntax/lint checks on modified PHP files
- `go test ./...` and `go build ./...` in agent-core

7. Rollout posture:
- keep legacy network channels allocator as fallback path
- enable canonical allocations by data presence, not by flag day cutover

## Deliverables of Phase 1

1. Canonical schema artifacts (`panel_nodes`, `allocations`) with idempotent migration.
2. Resource ledger hard-deny enforcement.
3. First-available allocator service and provisioning integration.
4. Strict runtime limits envelope passed end-to-end.
5. Additive proto contract update and regenerated stubs.
