---
id: panel-core-contributing
cluster: novus-os
category: panel-core-general
order: 100
status: active
version: 0.1.0
title: 'Внесок у розвиток: Документація та контракти'
description: Правила синхронізації docs/ та API-контрактів із кодом.
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/CONTRIBUTING.md
managed_by: sync_private_docs
---
# Contributing: Documentation and Contracts

Правила підтримання `docs/` та контрактів API в актуальному стані разом із кодом.

## 1. Базові вимоги

- Один документ — один чіткий обсяг (scope).
- Не зберігайте тимчасові звіти в активній документації модулів.
- Використовуйте відносні та валідні внутрішні посилання.
- Англійська мова є канонічною для документації з архітектури, API та безпеки.

## 2. Обов'язкові оновлення

- Якщо змінюється `routes/api.php`, перегенеруйте та зафіксуйте у коміті:
  - `docs/api-reference/openapi_3.1.yaml`
  - `docs/api/openapi.json`
  - `docs/api/openapi.yaml`
  - `docs/api/openapi.public.yaml`
  - прохід синхронізації маршрутів/специфікацій за допомогою `tools/quality/route_spec_sync.php`
- Якщо змінюється `app/Services/*` або додається новий публічний сервіс, перегенеруйте та зафіксуйте у коміті:
  - `docs/functions/services_full_inventory.md`
- Якщо змінюється навігація, володіння маршрутами або підключені поверхні Vue, оновіть:
  - `docs/dev/product_surface_map.md`
  - пов'язані документи модулів у `docs/manual/`
- Якщо змінюється поведінка модуля, оновіть відповідний файл у `docs/manual/`.
- Якщо змінюється політика UI або i18n, оновіть `docs/dev/style_contract.md`, `docs/dev/i18n_policy.md` та пов'язані документи в `docs/dev/`.
- Якщо додається новий розділ документації, оновіть `docs/README.md`.
- Якщо вміст документації змінюється, перегенеруйте та зафіксуйте у коміті:
  - `docs/project_documentation_unified.md`
- Тимчасові плани та робочі нотатки слід розміщувати в `docs/dev/tasks/`, `docs/dev/cleanup/` або у файлах з датами в `docs/dev/`.
- Історичні аудити, нотатки щодо часових поясів та застарілі контракти мають бути перенесені до `docs/dev/archive/`.

## 3. Обов'язкові перевірки перед злиттям (Merge)

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

Перед релізом або масштабним рефакторингом додатково запустіть `bash tools/quality/run_gates.sh`.

Скрипт `tools/quality/run_gates.sh` регенерує ці артефакти та в середовищах з підтримкою git завершується з помилкою, якщо згенеровані файли не були зафіксовані (committed).

## 4. Правила стилю

- Формулюйте думки лаконічно та орієнтовано на реалізацію.
- Використовуйте стабільну термінологію для модулів, ендпоінтів, прав доступу та подій.
- Відокремлюйте фактичну поведінку від історичних приміток.
- Використовуйте блоки коду для команд та прикладів корисного навантаження (payload).
- Надавайте перевагу оновленню існуючої документації заміство створення паралельних документів зі спільними зонами відповідальності.
