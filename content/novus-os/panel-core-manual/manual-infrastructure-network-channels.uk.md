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
# Модуль: Network Channels

Розподілений пул каналів для виділення та призначення рантайм-ендпоїнтів.

## 1. Призначення

Network Channels визначають одиниці зовнішнього підключення (ip/port/protocol), які можуть бути призначені рантайм-екземплярам з обмеженнями за ролями та областями дії (scope).

Головні цілі:

- підтримувати багаторазово використовуваний пул каналів для кожного вузла;
- забезпечувати сумісність областей дії для призначень;
- підтримувати робочий процес перемикання primary/reserve.

Канонічна таблиця:

- novus_os.panel_network_channels

Ключові виміри:

- role: primary, reserve, client, sourcetv;
- bind_scope: all, game, service, web, matrix;
- assignment: assigned_nid (може бути NULL для вільних каналів).

## 2. Головні Компоненти

- App\Controllers\Api\NetworkChannelsController
- App\Services\Runtime\NetworkChannelsService
- App\Services\Runtime\InstancesService
- resources/js/modules/Services/views/ServicesIndex.vue

Відповідальність:

- контролер: захист автентифікації/прав та контракт ендпоїнта;
- сервіс: CRUD, пакетне створення, призначення, перемикання (swap) та зведення;
- сервіс екземплярів: валідація цілі призначення за nid та типом/матрицею.
- InstancesPanel: швидка панель (drawer) для керування пулом каналів та інтеграції майстра через preview-allocation.

## 3. API Surface

| Method | Path | Purpose |
|---|---|---|
| GET | /api/network-channels/list | Отримання списку каналів із фільтрами (node_agent_id, role, bind_scope, matrix_slug, assigned_nid, free_only, target_type). |
| GET | /api/network-channels/node-summary | Лічильники загальних/вільних/призначених каналів для кожного вузла. |
| POST | /api/network-channels/create | Створення одного каналу. |
| POST | /api/network-channels/create-batch | Пакетне створення каналів за діапазонами ip/port. |
| POST | /api/network-channels/assign | Призначення каналу на instance nid (з можливістю перевизначення ролі). |
| POST | /api/network-channels/unbind | Звільнення призначення каналу. |
| POST | /api/network-channels/update | Часткове оновлення полів каналу (scope/role/address/active/тощо). |
| POST | /api/network-channels/delete | М'яке видалення каналу (is_active=0, unbind). |
| POST | /api/network-channels/swap | Помінне переключення основного та резервного каналів для заданого instance nid. |
| POST | /api/network-channels/bulk-release | Масове розірвання прив'язки набору ідентифікаторів каналів за одну операцію. |
| GET | /api/network-channels/preview-allocation | Попередній перегляд розподілу хост-портів на основі матриці для майстра створення без збереження каналів. |

## 4. Логіка призначення

- призначення перевіряє область дії каналу (channel scope) щодо цільового екземпляра;
- первинна унікальність забезпечується для кожного nid шляхом пониження інших первинних каналів;
- підміна (swap) вимагає наявності як первинного, так і резервного каналів для цільового nid.

## 5. Безпека та дозволи

Дозволи контролера:

- list/node-summary: platform.instances.read OR platform.settings.manage OR access.dashboard.view;
- preview-allocation: platform.instances.read OR platform.instances.write OR platform.settings.manage;
- операції запису: platform.instances.write OR platform.settings.manage.

Операційні примітки:
- canonical table тепер provisioning'ится setup foundation как часть `db_os` runtime-registry surface;
- service-level `ensureTable()` остаётся defensive fallback для partial restore/legacy paths;
- дублікат ідентичності (node_agent_id, ip_address, host_port, protocol) є унікальним.

## 6. Режими збоїв

- id_required, nid_required, id_and_nid_required;
- channel_not_found;
- channel_scope_mismatch_for_instance;
- swap_requires_primary_and_reserve;
- варіанти create_failed/update_failed/bulk_release_failed.

## 7. Related Docs

- ../../api-reference/rest_endpoints.md
- instances.md
- matrices.md
- ../architecture/database_topology.md

## 8. Завантаження портів з урахуванням схем

`NetworkChannelsController::loadMatrixPorts(string $slug): array<int>` —
переписано під дві схеми `panel_matrices`:

1. **Modern**: `slug` + `manifest_json`. Запит
   `SELECT default_port, manifest_json FROM panel_matrices WHERE slug = ?`.
2. **Legacy**: унікальний ключ — `name`, маніфести в `custom_manifest_json`
   та/або `exposed_ports_json`. Fallback ітерується по рядках, зіставляє
   `LOWER(name) = LOWER(slug)` АБО `slugify(name) = slug`. Джерело порту
   за пріоритетом: `custom_manifest_json` → `exposed_ports_json`
   (`int` або `[{port}, …]`) → `default_port`.

Наявність колонок перевіряється один раз через `information_schema.COLUMNS`
зі static-кешем (метод `columnExists(\mysqli, $table, $col): bool`).
Це усуває помилки 500 у `previewAllocation` на legacy-схемі без зміни
ABI відповіді.
