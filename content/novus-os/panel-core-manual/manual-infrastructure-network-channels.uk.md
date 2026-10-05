---
id: panel-core-manual-infrastructure-network-channels
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: 'Модуль: Network Channels'
description: Розподілений пул каналів для динамічного виділення та призначення endpoint.
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/infrastructure/network_channels.md
managed_by: sync_private_docs
---
# Module: Network Channels

Розподілений пул каналів для виділення та призначення кінцевих точок (endpoint) під час виконання.

## 1. Purpose

Network Channels визначають одиниці зовнішнього підключення (ip/port/protocol), які можуть призначатися екземплярам середовища виконання з обмеженнями за ролями та областями дії (scope).

Основні цілі:

- підтримувати повторно використовуваний пул каналів для кожного вузла (node);
- забезпечувати сумісність областей дії для призначень;
- підтримувати робочий процес перемикання primary/reserve.

Канонічна таблиця:

- novus_os.panel_network_channels

Ключові виміри:

- role: primary, reserve, client, sourcetv;
- bind_scope: all, game, service, web, matrix;
- assignment: assigned_nid nullable для вільних каналів.

## 2. Main Components

- App\Controllers\Api\NetworkChannelsController
- App\Services\Runtime\NetworkChannelsService
- App\Services\Runtime\InstancesService
- resources/js/modules/Services/views/ServicesIndex.vue

Відповідальність:

- controller: перевірка автентифікації/прав доступу (guard) та контракт кінцевої точки;
- service: CRUD, масове створення, призначення, заміна та зведення (summary);
- instances service: валідація цілі призначення за nid та type/matrix.
- InstancesPanel: швидка висувна панель (drawer) для керування пулом каналів та інтеграції майстра налаштування через preview-allocation.

## 3. Поверхня API

| Метод | Шлях | Призначення |
|---|---|---|
| GET | /api/network-channels/list | Отримання списку каналів із фільтрами (node_agent_id, role, bind_scope, matrix_slug, assigned_nid, free_only, target_type). |
| GET | /api/network-channels/node-summary | Лічильники загальних/вільних/призначених каналів для кожного вузла. |
| POST | /api/network-channels/create | Створення одного каналу. |
| POST | /api/network-channels/create-batch | Пакетне створення каналів за діапазонами IP-адрес/портів. |
| POST | /api/network-channels/assign | Призначення каналу на nid екземпляра (з можливістю перевизначення ролі). |
| POST | /api/network-channels/unbind | Звільнення призначення каналу. |
| POST | /api/network-channels/update | Часткове оновлення полів каналу (scope/role/address/active/тощо). |
| POST | /api/network-channels/delete | М'яке видалення каналу (is_active=0, unbind). |
| POST | /api/network-channels/swap | Місцями основний та резервний канали для одного nid екземпляра. |
| POST | /api/network-channels/bulk-release | Масове звільнення набору ідентифікаторів каналів за одну операцію. |
| GET | /api/network-channels/preview-allocation | Попередній перегляд виділення хост-портів на основі матриці для майстра створення без збереження каналів. |

## 4. Логіка призначення

- призначення перевіряє область каналу (channel scope) відносно цільового екземпляра;
- первинна унікальність забезпечується для кожного nid шляхом зниження статусу інших первинних каналів;
- підміна (swap) вимагає наявності як первинного, так і резервного каналів для цільового nid.

## 5. Безпека та дозволи

Дозволи контролера:

- list/node-summary: platform.instances.read OR platform.settings.manage OR access.dashboard.view;
- preview-allocation: platform.instances.read OR platform.instances.write OR platform.settings.manage;
- операції запису: platform.instances.write OR platform.settings.manage.

Операційні примітки:
- canonical table тепер provisioning'ится setup foundation как часть `db_os` runtime-registry surface;
- service-level `ensureTable()` остаётся defensive fallback для partial restore/legacy paths;
- дублюючі ідентифікатори (node_agent_id, ip_address, host_port, protocol) є унікальними.

## 6. Режими збоїв

- id_required, nid_required, id_and_nid_required;
- channel_not_found;
- channel_scope_mismatch_for_instance;
- swap_requires_primary_and_reserve;
- варіанти create_failed/update_failed/bulk_release_failed.

## 7. Пов'язана документація

- ../../api-reference/rest_endpoints.md
- instances.md
- matrices.md
- ../architecture/database_topology.md

## 8. Завантаження портів з урахуванням схеми

`NetworkChannelsController::loadMatrixPorts(string $slug): array<int>` —
переписано під дві схеми `panel_matrices`:

1. **Modern**: `slug` + `manifest_json`. Запит
   `SELECT default_port, manifest_json FROM panel_matrices WHERE slug = ?`.
2. **Legacy**: унікальний ключ — `name`, маніфести в `custom_manifest_json`
   та/або `exposed_ports_json`. Fallback ітерується по рядках, зів'язує
   `LOWER(name) = LOWER(slug)` АБО `slugify(name) = slug`. Джерело порту
   за пріоритетом: `custom_manifest_json` → `exposed_ports_json`
   (`int` або `[{port}, …]`) → `default_port`.

Наявність колонок перевіряється один раз через `information_schema.COLUMNS`
зі статичним кешем (метод `columnExists(\mysqli, $table, $col): bool`).
Це усуває 500 помилку у `previewAllocation` на legacy-схемі без зміни
ABI відповіді.
