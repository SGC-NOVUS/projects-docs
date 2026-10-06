---
id: agent-core-api
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Довідник gRPC API'
description: '**Джерело контракту:** proto/novus.proto та proto/novus_runtime_surface.proto.
  Номери полів, структури повідомлень та методи сервісів у цих файлах є авторитетними.
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

**Джерело контракту:** `proto/novus.proto` та `proto/novus_runtime_surface.proto`. Номери полів, форми повідомлень і методи сервісів у цих файлах є авторитетними. Ця сторінка є безпечним довідником для навігації, а не заною згенерованих клієнтів protobuf.

## Транспорт і доступ

- Транспортом є gRPC поверх TLS.
- Звичайні привілейовані виклики містять метадані `x-request-timestamp`, `x-signature` та `x-panel-uuid`.
- Агент застосовує блокування сполученої панелі (Panel), перевірку свіжості запитів, захист від повтору (Replay Guard), ліміти запитів (rate limits) і політику аудиту перед диспетчеризацією привілейованих викликів.
- Сполучення (Pairing) та стандартні перевірки працездатності gRPC є винятками для ініціалізації (bootstrap) та перевірки живої системи (liveness). Не реалізуйте клієнт лише на основі цього документа; використовуйте підтримуваний транспорт Panel або згенеровану інтеграцію protobuf.

## NovusAgent

| Метод | Взаємодія | Призначення |
| --- | --- | --- |
| `AgentTelemetry` | Unary | Збирає телеметрію ЦП, пам'яті та диска хоста. |
| `DockerManager` | Unary | Виконує дозволену дію життєвого циклу для контейнера виконання. |
| `PtyStream` | Двосторонній потік (Bidirectional stream) | Передає авторизовану сесію термінала. |
| `RotateMasterSecret` | Unary | Ротує секрет зв'язку сполученої панелі з агентом (Panel-to-Agent). |
| `PairNode` | Unary | Прив'язує несполучений агент до однієї панелі за допомогою схваленого потоку сполучення. |
| `UnclaimNode` | Unary | Видаляє поточну прив'язку панелі. |
| `UpdateAgent` | Unary | Запитує підтримуваний робочий процес оновлення агента. |

Кадри `PtyStream` використовують корисне навантаження (payloads) `open`, `input`, `resize`, `output`, `exit` та `error`. Початковий кадр клієнта повинен відкрити сесію. Вибір оболонки обмежений конфігурацією агента; браузери ніколи не отримують прямого доступу до хост-PTY.

## InstanceService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateInstance` | Server stream | Забезпечує розгортання ігрового, сервісного чи веб-середовища виконання та передає потоком хід виконання. |
| `ReinstallInstance` | Server stream | Перевстановлює наявний екземпляр, використовуючи поточні метадані та значення за замовчуванням матриці. |
| `CheckPorts` | Unary | Перевіряє пул кандидатів портів середовища виконання. |
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

`ContainerFsPull` є серверним потоком. Методи вебсайту надають доступ до метаданих сертифікатів; випуск та оновлення сертифікатів не є методами поточного контракту `NovusRuntimeSurface`.

## Правила сумісності

- Додавання нових полів та методів protobuf вимагає узгодженого планування випуску для Agent, кодека/клієнта Panel, тестів.
- Заборонено самостійно перейменовувати поля, змінювати номери полів, змінювати назви метаданих або порушувати порядок потоків (stream ordering).
- `NovusFileSystem` існує в `proto/novus_fs.proto`, проте наразі це не зареєстрована поверхня сервісу. Не використовуйте його як підтримувану середовищем виконання кінцеву точку (endpoint), доки не буде завершено реєстрацію та документацію сумісності.

## Помилки

Обробники використовують стандартні коди статусу gRPC. Клієнти повинні обробляти принаймні `InvalidArgument`, `Unauthenticated`, `PermissionDenied`, `FailedPrecondition`, `Unavailable`, `ResourceExhausted` і `Internal`, а також відображати безпечне для користувача повідомлення через Panel замість розкриття сирих деталей хоста.
