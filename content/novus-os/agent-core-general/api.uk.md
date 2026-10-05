---
id: agent-core-api
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Довідник gRPC API'
description: '**Contract source:** proto/novus.proto та proto/novus_runtime_surface.proto.
  Номера полів, форми повідомлень та методи сервісів у цих файлах є авторитетними.
  Ця сторінка є...'
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/API.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core: gRPC API Reference

**Джерело контракту:** `proto/novus.proto` та `proto/novus_runtime_surface.proto`. Номери полів, структури повідомлень і методи сервісів у цих файлах є авторитетними. Ця сторінка є безпечним навігаційним довідником, а не заною згенерованим клієнтам protobuf.

## Транспорт і доступ

- Транспортом є gRPC поверх TLS.
- Звичайні привілейовані виклики містять метадані `x-request-timestamp`, `x-signature` та `x-panel-uuid`.
- Agent застосовує блокування сполученої Panel, перевірку свіжості запитів, захист від повтору (replay), обмеження швидкості (rate limits) та політику аудиту перед диспетчеризацією привілейованих викликів.
- Сполучення (Pairing) та стандартні перевірки працездатності gRPC є винятками для ініціалізації та перевірки життєздатності (liveness). Не реалізуйте клієнт лише на основі цього документа; використовуйте підтримуваний транспорт Panel або згенеровану інтеграцію protobuf.

## NovusAgent

| Метод | Взаємодія | Призначення |
| --- | --- | --- |
| `AgentTelemetry` | Унарний | Збирає телеметрію процесора, пам'яті та диска хоста. |
| `DockerManager` | Унарний | Виконує дозволену дію життєвого циклу для контейнера виконання. |
| `PtyStream` | Двосторонній потік | Передає авторизовану сесію термінала. |
| `RotateMasterSecret` | Унарний | Ротує секрет між сполученими Panel та Agent. |
| `PairNode` | Унарний | Прив'язує несполучений Agent до однієї Panel за допомогою затвердженого процесу сполучення. |
| `UnclaimNode` | Унарний | Видаляє поточну прив'язку Panel. |
| `UpdateAgent` | Унарний | Запитує підтримуваний робочий процес оновлення Agent. |

Фрейми `PtyStream` використовують корисне навантаження (payloads) `open`, `input`, `resize`, `output`, `exit` і `error`. Початковий фрейм клієнта повинен відкрити сесію. Вибір оболонки обмежений конфігурацією Agent; браузери ніколи не отримують прямого доступу до PTY хоста.

## InstanceService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateInstance` | Server stream | Створює екземпляр гри, сервісу чи вебсередовища виконання та передає потоком хід виконання. |
| `ReinstallInstance` | Server stream | Перевстановлює наявний екземпляр, використовуючи поточні метадані та значення за замовчуванням матриці. |
| `CheckPorts` | Unary | Перевіряє пул потенційних портів середовища виконання. |
| `AllocatePorts` | Unary | Атомарно резервує доступний пул портів. |

## BackupService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateBackup` | Server stream | Створює архів резервної копії екземпляра та передає потоком хід виконання. |
| `RestoreBackup` | Server stream | Відновлює резервну копію в екземпляр та передає потоком хід виконання. |
| `DeleteBackup` | Unary | Видаляє резервну копію з вибраного адаптера. |
| `ListBackups` | Unary | Виводить список метаданих резервних копій для екземпляра. |

## NovusRuntimeSurface

| Area | Methods |
| --- | --- |
| Host and runtime inventory | `HostInfo`, `RuntimeContainers` |
| VFS | `VfsList`, `VfsStat`, `VfsRead`, `VfsWrite`, `VfsDelete`, `VfsChmod`, `VfsMove`, `VfsCopy`, `VfsMkdir`, `VfsCompress`, `VfsExtract`, `VfsUploadInit`, `VfsUploadChunk`, `VfsUploadFinalize` |
| Container lifecycle | `RuntimeContainerInspect`, `RuntimeContainerStats`, `RuntimeContainerCreate`, `RuntimeContainerRemove` |
| Container filesystem | `ContainerFsList`, `ContainerFsRead`, `ContainerFsWrite`, `ContainerFsMkdir`, `ContainerFsDelete`, `ContainerFsRename`, `ContainerFsPull` |
| Website certificate metadata | `WebsiteSslCertificates`, `WebsiteSslCertificate` |

`ContainerFsPull` є серверним потоком (server stream). Методи вебсайту надають метадані сертифікатів; випуск та оновлення сертифікатів не є методами поточного контракту `NovusRuntimeSurface`.

## Правила сумісності

- Додавання нових полів та методів protobuf вимагає скоординованого планування для Agent, кодека/клієнта Panel, тестів та випуску релізів.
- Заборонено самостійно перейменовувати поля, змінювати номери полів, змінювати назви метаданих або змінювати порядок потоків (stream ordering).
- `NovusFileSystem` існує в `proto/novus_fs.proto`, проте наразі він не є зареєстрованою поверхнею сервісу. Не використовуйте його як підтримувану точку підключення (runtime endpoint), доки не буде завершено реєстрацію та документацію щодо сумісності.

## Помилки

Обробники використовують стандартні коди статусу gRPC. Клієнти повинні обробляти принаймні `InvalidArgument`, `Unauthenticated`, `PermissionDenied`, `FailedPrecondition`, `Unavailable`, `ResourceExhausted` та `Internal`, а також відображати безпечне для користувача повідомлення через Panel, замість того щоб розкривати деталі хоста.
