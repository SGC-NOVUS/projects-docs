---
id: agent-core-readme
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: Документация NOVUS Agent-Core
description: '**Version:** 0.2.0 **Language:** Go 1.25 **Purpose:** Аутентифицированная
  среда выполнения узла NOVUS OS для одобренных локальных задач хоста.'
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/README.md
managed_by: sync_private_docs
---
# Документация NOVUS Agent-Core

**Версия:** 0.2.0  
**Язык:** Go 1.25  
**Назначение:** Среда выполнения аутентифицированного узла NOVUS OS для разрешенных локальных задач хоста.

## Документация

| Документ | Описание |
| --- | --- |
| [getting-started/README.md](getting-started/README.md) | Безопасный первый путь для операторов |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Сервисы агента, компоненты и поток данных |
| [API.md](API.md) | Справочник по gRPC API |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Безопасный жизненный цикл развертывания |
| [SECURITY.md](SECURITY.md) | Модель аутентификации, транспорта и аудита |
| [CONFIGURATION.md](CONFIGURATION.md) | Поддерживаемая поверхность конфигурации |
| [VFS.md](VFS.md) | Модель изолированной виртуальной файловой системы |
| [PAIRING.md](PAIRING.md) | Аутентифицированное сопряжение панели с агентом |

Внутренние инженерные журналы ведутся в `docs/dev` и исключены из публикации публичной документации.

## Лицензия

Проприетарное ПО. Все права защищены SGC-NOVUS.
