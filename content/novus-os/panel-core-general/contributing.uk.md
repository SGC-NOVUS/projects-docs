---
id: panel-core-contributing
cluster: novus-os
category: panel-core-general
order: 100
status: active
version: 0.1.0
title: 'Внесок: Документація та Контракти'
description: Правила підтримання синхронізації `docs/` та API-контрактів із кодом.
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/CONTRIBUTING.md
managed_by: sync_private_docs
---
# Участь у розробці: Документація та контракти

Правила підтримання `docs/` та API-контрактів у синхронізованому з кодом стані.

## 1. Базові вимоги

- Один документ — один чіткий обсяг завдань (scope).
- Не зберігайте тимчасові звіти в активній документації модулів.
- Використовуйте відносні та дійсні внутрішні посилання.
- Англійська мова є канонічною для документації з архітектури, API та безпеки.

## 2. Обов'язкові оновлення

- Якщо змінюється `routes/api.php`, перегенерація та коміт обов'язкові для:
  - `docs/api-reference/openapi_3.1.yaml`
  - `docs/api/openapi.json`
  - `docs/api/openapi.yaml`
  - `docs/api/openapi.public.yaml`
  - проходження синхронізації маршрутів/специфікацій через `tools/quality/route_spec_sync.php`
- Якщо змінюється `app/Services/*` або додається новий публічний сервіс, перегенерація та коміт обов'язкові для:
  - `docs/functions/services_full_inventory.md`
- Якщо змінюється навігація, володіння маршрутами чи підключені поверхні Vue, оновіть:
  - `docs/dev/product_surface_map.md`
  - пов'язані документи модуля в `docs/manual/`
- Якщо змінюється поведінка модуля, оновіть пов'язаний файл у `docs/manual/`.
- Якщо змінюється політика UI або i18n, оновіть `docs/dev/style_contract.md`, `docs/dev/i18n_policy.md` та пов'язані документи в `docs/dev/`.
- Якщо додається новий розділ документації, оновіть `docs/README.md`.
- Якщо вміст документації змінюється, перегенерація та коміт обов'язкові для:
  - `docs/project_documentation_unified.md`
- Тимчасові плани та робочі нотатки мають розміщуватися в `docs/dev/tasks/`, `docs/dev/cleanup/` або у файлах з датами в `docs/dev/`.
- Історичні аудити, нотатки щодо часових поясів та застарілі контракти необхідно розміщувати в `docs/dev/archive/`.

## 3. Required Checks Before Merge

```bash
php tools/openapi/generate_openapi.php
php tools/audit/services_inventory.php
npm run docs:unified
php tools/quality/route_spec_sync.php
php tools/quality/openapi_split_guard.php
node tools/quality/docs_contract_coverage_check.mjs
node tools/quality/i18n_parity.mjs --strict
node tools/quality/no_local_vue_styles.mjs
php tools/quality/docs_link_check.php
bash tools/quality/run_fast_gates.sh
```

Перед релізом або великими рефакторингами додатково запустіть `bash tools/quality/run_gates.sh`.

`tools/quality/run_gates.sh` регенерує ці артефакти та в середовищах із підтримкою git завершується помилкою, якщо згенеровані файли не були зафіксовані (commit).

## 4. Style Rules

- Формулюйте думки лаконічно та орієнтовано на реалізацію.
- Використовуйте стабільну термінологію для модулів, ендпоінтів, дозволів і подій.
- Відокремлюйте фактичну поведінку від історичних нотаток.
- Використовуйте блоки коду для команд та прикладів корисного навантаження (payload).
- Надавайте перевагу оновленню наявної документації, а не створенню паралельних документів із перетином зон відповідальності.
