---
id: agent-core-readme
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: Документація NOVUS Agent-Core
description: '**Version:** 0.2.0 **Language:** Go 1.25 **Purpose:** Автентифіковане
  середовище виконання вузла NOVUS OS для дозволеної локальної роботи на хості.'
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/README.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core Documentation

**Version:** 0.2.0  
**Language:** Go 1.25  
**Purpose:** Авторизоване середовище виконання ноди NOVUS OS для затвердженої локальної роботи на хості.

## Documentation

| Document | Description |
| --- | --- |
| [getting-started/README.md](getting-started/README.md) | Безпечний початковий шлях для операторів |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Служби агента, компоненти та потік даних |
| [API.md](API.md) | Довідник gRPC API |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Безпечний життєвий цикл розгортання |
| [SECURITY.md](SECURITY.md) | Модель автентифікації, транспорту та аудиту |
| [CONFIGURATION.md](CONFIGURATION.md) | Підтримувана поверхня конфігурації |
| [VFS.md](VFS.md) | Модель обмеженої віртуальної файлової системи |
| [PAIRING.md](PAIRING.md) | Авторизоване з'єднання панелі з агентом (Panel-to-Agent) |

Внутрішні інженерні записи ведуться в `docs/dev` та виключені з публікації загальнодоступної документації.

## License

Пропрієтарно. Усі права захищені SGC-NOVUS.
