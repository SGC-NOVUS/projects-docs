---
id: panel-core-manual-infrastructure-network-channels
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: 'Module: Network Channels'
description: Distributed channel pool for runtime endpoint allocation and assignment.
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/network_channels.md
managed_by: sync_private_docs
---
# Module: Network Channels

Distributed channel pool for runtime endpoint allocation and assignment.

## 1. Purpose

Network Channels define external connectivity units (ip/port/protocol) that can be assigned to runtime instances with role and scope constraints.

Main goals:

- keep a reusable channel pool per node;
- enforce scope compatibility for assignments;
- support primary/reserve switch workflow.

Canonical table:

- novus_os.panel_network_channels

Key dimensions:

- role: primary, reserve, client, sourcetv;
- bind_scope: all, game, service, web, matrix;
- assignment: assigned_nid nullable for free channels.

## 2. Main Components

- App\Controllers\Api\NetworkChannelsController
- App\Services\Runtime\NetworkChannelsService
- App\Services\Runtime\InstancesService
- resources/js/modules/Services/views/ServicesIndex.vue

Responsibilities:

- controller: auth/permission guard and endpoint contract;
- service: CRUD, batch creation, assignment, swap and summary;
- instances service: assignment target validation by nid and type/matrix.
- InstancesPanel: quick drawer for channel pool controls and wizard integration via preview-allocation.

## 3. API Surface

| Method | Path | Purpose |
|---|---|---|
| GET | /api/network-channels/list | List channels with filters (node_agent_id, role, bind_scope, matrix_slug, assigned_nid, free_only, target_type). |
| GET | /api/network-channels/node-summary | Per-node total/free/assigned counters. |
| POST | /api/network-channels/create | Create one channel. |
| POST | /api/network-channels/create-batch | Batch create channels by ip/port ranges. |
| POST | /api/network-channels/assign | Assign channel to instance nid (optional role override). |
| POST | /api/network-channels/unbind | Release assignment from channel. |
| POST | /api/network-channels/update | Patch channel fields (scope/role/address/active/etc). |
| POST | /api/network-channels/delete | Soft-delete channel (is_active=0, unbind). |
| POST | /api/network-channels/swap | Swap primary and reserve channels for one instance nid. |
| POST | /api/network-channels/bulk-release | Unbind a set of channel ids in one operation. |
| GET | /api/network-channels/preview-allocation | Preview matrix-driven host port allocation for the create wizard without persisting channels. |

## 4. Assignment Logic

- assignment validates channel scope against target instance;
- primary uniqueness is enforced per nid by demoting other primary channels;
- swap requires both primary and reserve channels for target nid.

## 5. Security and Permissions

Controller permissions:

- list/node-summary: platform.instances.read OR platform.settings.manage OR access.dashboard.view;
- preview-allocation: platform.instances.read OR platform.instances.write OR platform.settings.manage;
- write operations: platform.instances.write OR platform.settings.manage.

Operational notes:
- canonical table теперь provisioning'ится setup foundation как часть `db_os` runtime-registry surface;
- service-level `ensureTable()` остаётся defensive fallback для partial restore/legacy paths;
- duplicate identity (node_agent_id, ip_address, host_port, protocol) is unique.

## 6. Failure Modes

- id_required, nid_required, id_and_nid_required;
- channel_not_found;
- channel_scope_mismatch_for_instance;
- swap_requires_primary_and_reserve;
- create_failed/update_failed/bulk_release_failed variants.

## 7. Related Docs

- ../../api-reference/rest_endpoints.md
- instances.md
- matrices.md
- ../architecture/database_topology.md

## 8. Schema-aware port loading

`NetworkChannelsController::loadMatrixPorts(string $slug): array<int>` —
переписан под две схемы `panel_matrices`:

1. **Modern**: `slug` + `manifest_json`. Запрос
   `SELECT default_port, manifest_json FROM panel_matrices WHERE slug = ?`.
2. **Legacy**: уникальный ключ — `name`, манифесты в `custom_manifest_json`
   и/или `exposed_ports_json`. Fallback итерируется по строкам, матчит
   `LOWER(name) = LOWER(slug)` ИЛИ `slugify(name) = slug`. Источник порта
   в приоритете: `custom_manifest_json` → `exposed_ports_json`
   (`int` или `[{port}, …]`) → `default_port`.

Наличие колонок проверяется один раз через `information_schema.COLUMNS`
со static-кешем (метод `columnExists(\mysqli, $table, $col): bool`).
Это снимает 500 в `previewAllocation` на legacy-схеме без изменения
ABI ответа.
