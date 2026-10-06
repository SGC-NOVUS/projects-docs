---
id: panel-core-manual-infrastructure-network-channels
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: 'Модуль: Network Channels'
description: Распределенный пул каналов для выделения и назначения эндпоинтов во время
  выполнения.
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/network_channels.md
managed_by: sync_private_docs
---
# Модуль: Network Channels

Распределенный пул каналов для выделения и назначения эндпоинтов во время выполнения (runtime).

## 1. Назначение

Network Channels определяют внешние единицы подключения (ip/port/protocol), которые могут назначаться инстансам во время выполнения с ограничениями по роли и области видимости (scope).

Основные цели:

- поддерживать повторно используемый пул каналов для каждого нода (node);
- обеспечивать соблюдение совместимости областей видимости для назначений;
- поддерживать рабочий процесс переключения primary/reserve.

Каноническая таблица:

- novus_os.panel_network_channels

Ключевые измерения:

- role: primary, reserve, client, sourcetv;
- bind_scope: all, game, service, web, matrix;
- assignment: assigned_nid (пускает null для свободных каналов).

## 2. Основные компоненты

- App\Controllers\Api\NetworkChannelsController
- App\Services\Runtime\NetworkChannelsService
- App\Services\Runtime\InstancesService
- resources/js/modules/Services/views/ServicesIndex.vue

Зоны ответственности:

- контроллер: проверка авторизации/прав и контракт эндпоинта;
- сервис: CRUD, пакетное создание, назначение, замена (swap) и сводка;
- сервис инстансов: валидация цели назначения по nid, типу и матрице.
- InstancesPanel: быстрая боковая панель для управления пулом каналов и интеграции мастера через предварительное выделение (preview-allocation).

## 3. API Surface

| Method | Path | Purpose |
|---|---|---|
| GET | /api/network-channels/list | Получение списка каналов с фильтрами (node_agent_id, role, bind_scope, matrix_slug, assigned_nid, free_only, target_type). |
| GET | /api/network-channels/node-summary | Счетчики общего количества/свободных/назначенных каналов в разрезе нод. |
| POST | /api/network-channels/create | Создание одного канала. |
| POST | /api/network-channels/create-batch | Пакетное создание каналов по диапазонам IP-адресов/портов. |
| POST | /api/network-channels/assign | Назначение канала на instance nid (с опциональным переопределением роли). |
| POST | /api/network-channels/unbind | Снятие назначения с канала. |
| POST | /api/network-channels/update | Частичное обновление полей канала (scope/role/address/active/и т. д.). |
| POST | /api/network-channels/delete | Логическое удаление канала (is_active=0, сброс назначения). |
| POST | /api/network-channels/swap | Меняет местами основной и резервный каналы для заданного instance nid. |
| POST | /api/network-channels/bulk-release | Массовое снятие назначения с набора идентификаторов каналов за одну операцию. |
| GET | /api/network-channels/preview-allocation | Предварительный просмотр распределения хост-портов на основе матриц для мастера создания без сохранения каналов в базе данных. |

## 4. Логика назначения

- assignment проверяет область видимости (scope) канала по отношению к целевому экземпляру (target instance);
- первичная уникальность обеспечивается для каждого nid путем понижения статуса остальных первичных каналов;
- swap требует наличия как первичного, так и резервного каналов для целевого nid.

## 5. Безопасность и права доступа

Права контроллера:

- list/node-summary: platform.instances.read OR platform.settings.manage OR access.dashboard.view;
- preview-allocation: platform.instances.read OR platform.instances.write OR platform.settings.manage;
- операции записи (write operations): platform.instances.write OR platform.settings.manage.

Эксплуатационные примечания:
- canonical table теперь provisioning'ится setup foundation как часть `db_os` runtime-registry surface;
- service-level `ensureTable()` остаётся defensive fallback для partial restore/legacy paths;
- duplicate identity (node_agent_id, ip_address, host_port, protocol) is unique.

## 6. Режимы отказов

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
   и/или `exposed_ports_json`. Fallback итерируется по строкам, матчит
   `LOWER(name) = LOWER(slug)` ИЛИ `slugify(name) = slug`. Источник порта
   в приоритете: `custom_manifest_json` → `exposed_ports_json`
   (`int` или `[{port}, …]`) → `default_port`.

Наличие колонок проверяется один раз через `information_schema.COLUMNS`
со static-кешем (метод `columnExists(\mysqli, $table, $col): bool`).
Это снимает 500 в `previewAllocation` на legacy-схеме без изменения
ABI ответа.
