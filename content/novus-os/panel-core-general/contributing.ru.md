---
id: panel-core-contributing
cluster: novus-os
category: panel-core-general
order: 100
status: active
version: 0.1.0
title: 'Вклад в проект: Документация и контракты'
description: Правила синхронизации документации в каталоге docs/ и контрактов API
  с кодом.
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/CONTRIBUTING.md
managed_by: sync_private_docs
---
# Участие в разработке: Документация и контракты

Правила поддержания `docs/` и API-контрактов в актуальном состоянии вместе с кодом.

## 1. Базовые принципы

- Один документ — одна четкая область видимости.
- Не храните временные отчеты в документации активных модулей.
- Держите внутренние ссылки относительными и рабочими.
- Английский язык является каноническим для документации по архитектуре, API и безопасности.

## 2. Обязательные обновления

- Если изменяется `routes/api.php`, пересоздайте и закоммитьте:
  - `docs/api-reference/openapi_3.1.yaml`
  - `docs/api/openapi.json`
  - `docs/api/openapi.yaml`
  - `docs/api/openapi.public.yaml`
  - прогон синхронизации маршрутов и спецификаций через `tools/quality/route_spec_sync.php`
- Если изменяется `app/Services/*` или добавляется новый публичный сервис, пересоздайте и закоммитьте:
  - `docs/functions/services_full_inventory.md`
- Если изменяется навигация, владение маршрутами или подключаемые интерфейсы на Vue, обновите:
  - `docs/dev/product_surface_map.md`
  - соответствующую документацию модуля в `docs/manual/`
- Если изменяется поведение модуля, обновите соответствующий файл в `docs/manual/`.
- Если изменяется политика UI или i18n, обновите `docs/dev/style_contract.md`, `docs/dev/i18n_policy.md` и связанные документы в `docs/dev/`.
- Если добавляется новый раздел документации, обновите `docs/README.md`.
- Если содержимое документации изменяется, пересоздайте и закоммитьте:
  - `docs/project_documentation_unified.md`
- Временные планы и рабочие заметки должны находиться в `docs/dev/tasks/`, `docs/dev/cleanup/` или в файлах с датами в `docs/dev/`.
- Исторические аудиты, примечания о часовых поясах и устаревшие контракты должны размещаться в `docs/dev/archive/`.

## 3. Обязательные проверки перед слиянием

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

Перед релизом или масштабными рефакторингами дополнительно запускайте `bash tools/quality/run_gates.sh`.

Скрипт `tools/quality/run_gates.sh` пересоздает эти артефакты и в средах с поддержкой git завершается с ошибкой, если сгенерированные файлы не были зафиксированы в коммите.

## 4. Правила стиля

- Формулировки должны быть лаконичными и ориентированными на реализацию.
- Используйте стабильную терминологию для модулей, endpoints, прав доступа и событий.
- Отделяйте фактическое поведение от исторических заметок.
- Используйте блоки кода для команд и примеров полезной нагрузки (payload).
- Предпочитайте обновление существующей документации созданию параллельных документов с пересекающейся зоной ответственности.
