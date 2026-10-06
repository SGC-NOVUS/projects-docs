---
id: panel-core-getting-started-readme
cluster: novus-os
category: panel-core-getting-started
order: 100
status: active
version: 0.1.0
title: Начало работы с NOVUS-OS Panel
description: Панель NOVUS-OS является Control-Plane платформы. Она предоставляет рабочее
  пространство браузера для пользователей и операторов, делегируя привилегированную
  работу с хостом аутентифицированному NOVUS A...
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/getting-started/README.md
managed_by: sync_private_docs
---
# Начало работы с NOVUS-OS Panel

NOVUS-OS Panel — это Control-Plane платформы. Она предоставляет рабочее пространство браузера для пользователей и операторов, делегируя привилегированную работу с хостом аутентифицированному NOVUS Agent.

## Первая сессия

1. Откройте утвержденный URL Panel, предоставленный вашим администратором.
2. Войдите в систему под выданной вам учетной записью и пройдите необходимую многофакторную верификацию.
3. Начните с **Dashboard** для просмотра доступных нод, служб, алертов и операционных задач.
4. Открывайте функциональный модуль только тогда, когда назначенные вам разрешения позволяют выполнять этот рабочий процесс.

## Основные рабочие процессы

| Цель | Руководство |
| --- | --- |
| Просмотр служб и инстансов | [Infrastructure: Instances](../manual/infrastructure/instances.md) |
| Работа с управляемыми файлами | [Infrastructure: VFS](../manual/infrastructure/vfs.md) |
| Просмотр резервных копий | [Resources: Backups](../manual/resources/backups.md) |
| Управление веб-сайтами и сетевыми ресурсами | [Infrastructure: Network](../manual/infrastructure/network.md) |
| Использование доступа к терминалу | [UI Guide: Terminal](../manual/ui_guide/terminal.md) |
| Понимание разрешений и безопасности | [System: Permission Guard](../manual/system/permission_guard.md) |

## Границы безопасности

Panel не является прямой корневой оболочкой (root shell). Операции с хостом, рантаймом, файловой системой и терминалом авторизуются Panel и выполняются через транспорт Agent. Не пытайтесь заменять рабочие процессы продукта командами на стороне браузера, скопированными токенами или прямым доступом к хосту.

Для разработчиков начните с [Architecture Overview](../dev/architecture_overview.md). Для интеграции через API используйте проверенный контракт в [OpenAPI 3.1](../api-reference/openapi_3.1.yaml).
