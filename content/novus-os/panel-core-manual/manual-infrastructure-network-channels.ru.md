---
id: panel-core-manual-infrastructure-network-channels
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: 'Модуль: Network Channels'
description: Распределенный пул каналов для динамического выделения и назначения endpoint.
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/network_channels.md
managed_by: sync_private_docs
---
# Module: Network Channels

Distributed channel pool for runtime endpoint allocation and assignment.

## 1. Purpose

Network Channels определяющие внешние модули подключения (ip/port/protocol), которые могут быть назначены экземплярам runtime с ограничениями по роли и области видимости (scope).

Main goals:

- поддержка повторно используемого пула каналов для каждого узла (node);
- контроль совместимости областей видимости (scope) для назначений;
- поддержка рабочего процесса переключения основной/резервной роли (primary/reserve switch).

Canonical table:

- novus_os.panel_network_channels

Key dimensions:

- role: primary, reserve, client, sourcetv;
- bind_scope: all, game, service, web, matrix;
- assignment: assigned_nid nullable для свободных каналов.

## 2. Main Components

- App\Controllers\Api\NetworkChannelsController
- App\Services\Runtime\NetworkChannelsService
- App\Services\Runtime\InstancesService
- resources/js/modules/Services/views/ServicesIndex.vue

Responsibilities:

- controller: проверка авторизации/прав и контракт эндпоинта;
- service: CRUD, пакетное создание, назначение, замена и сводка;
- instances service: проверка цели назначения по nid и типу/matrix.
- InstancesPanel: бымая панель (drawer) для управления пулом каналов и интеграции мастера (wizard) через preview-allocation.

## 3. API Surface

| Method | Path | Purpose |
|---|---|---|
| GET | /api/network-channels/list | Получение списка каналов с фильтрами (node_agent_id, role, bind_scope, matrix_slug, assigned_nid, free_only, target_type). |
| GET | /api/network-channels/node-summary | Счетчики общего/свободного/назначенного количества в разрезе нод. |
| POST | /api/network-channels/create | Создание одного канала. |
| POST | /api/network-channels/create-batch | Пакетное создание каналов по диапазонам ip/port. |
| POST | /api/network-channels/assign | Назначение канала на nid инстанса (с опциональным переопределением роли). |
| POST | /api/network-channels/unbind | Снятие назначения с канала. |
| POST | /api/network-channels/update | Частичное обновление полей канала (scope/role/address/active и т. д.). |
| POST | /api/network-channels/delete | Логическое удаление канала (is_active=0, сброс назначения). |
| POST | /api/network-channels/swap | Меняет местами основной и резервный каналы для заданного nid инстанса. |
| POST | /api/network-channels/bulk-release | Массовое отвязывание набора идентификаторов каналов за одну операцию. |
| GET | /api/network-channels/preview-allocation | Предварительный просмотр выделения хостовых портов на основе матриц для мастера создания без сохранения каналов. |

## 4. Логика назначения

- assignment проверяет область видимости канала (channel scope) по отношению к целевому экземпляру (target instance);
- первичная уникальность (primary uniqueness) обеспечивается для каждого nid путем понижения статуса других первичных каналов;
- swap требует наличия как первичного, так и резервного каналов для целевого nid.

## 5. Безопасность и права доступа

Права доступа контроллера:

- list/node-summary: platform.instances.read OR platform.settings.manage OR access.dashboard.view;
- preview-allocation: platform.instances.read OR platform.instances.write OR platform.settings.manage;
- операции записи (write operations): platform.instances.write OR platform.settings.manage.

Операционные примечания:
- canonical table теперь provisioning'ится setup foundation как часть `db_os` runtime-registry surface;
- service-level `ensureTable()` остаётся defensive fallback для partial restore/legacy paths;
- дублирующиеся идентификационные данные (node_agent_id, ip_address, host_port, protocol) уникальны.

## 6. Режимы сбоев

- id_required, nid_required, id_and_nid_required;
- channel_not_found;
- channel_scope_mismatch_for_instance;
- swap_requires_primary_and_reserve;
- варианты create_failed/update_failed/bulk_release_failed.

## 7. Связанная документация

- ../../api-reference/rest_endpoints.md
- instances.md
- matrices.md
- ../architecture/database_topology.md

## 8. Загрузка портов с учетом схем

`NetworkChannelsController::loadMatrixPorts(string $slug): array<int>` —
переписан под две схемы `panel_matrices`:

1. **Modern**: `slug` + `manifest_json`. Запрос
   `SELECT default_port, manifest_json FROM panel_matrices WHERE slug = ?`.
2. **Legacy**: уникальный ключ — `name`, манифесты в `custom_manifest_json`
   и/или `exposed_ports_json`. Fallback итерируется по строкам, сопоставляет
   `LOWER(name) = LOWER(slug)` ИЛИ `slugify(name) = slug`. Источник порта
   в приоритете: `custom_manifest_json` → `exposed_ports_json`
   (`int` или `[{port}, …]`) → `default_port`.

Наличие колонок проверяется один раз через `information_schema.COLUMNS`
со static-кешем (метод `columnExists(\mysqli, $table, $col): bool`).
Это устраняет ошибку 500 в `previewAllocation` на legacy-схеме без изменения
ABI ответа.
