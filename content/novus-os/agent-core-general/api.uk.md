---
id: agent-core-api
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Довідник gRPC API'
description: '**Contract source:** proto/novus.proto та proto/novus_runtime_surface.proto.
  Номера полів, формати повідомлень і методи сервісів у цих файлах є авторитетними.
  Ця сторінка є...'
last_updated: '2026-10-02'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/API.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core: gRPC API Reference

**Contract source:** `proto/novus.proto` і `proto/novus_runtime_surface.proto`. Номери полів, структури повідомлень і сервісні методи в цих файлах є авторитетними. Ця сторінка є безпечним довідником для навігації, а не заміною згенерованих клієнтів protobuf.

## Transport And Access

- Транспорт — це gRPC через TLS.
- Звичайні привілейовані виклики містять метадані `x-request-timestamp`, `x-signature` та `x-panel-uuid`.
- Agent застосовує своє блокування пов'язаного Panel, свіжість запитів, захист від повтору (Replay Guard), ліміти запитів і політику аудиту перед диспетчеризацією привілейованих викликів.
- Сполучення (Pairing) та стандартні перевірки працездатності gRPC є винятками для ініціалізації та перевірки життєздатності (liveness). Не реалізуйте клієнта лише на основі цього документа; використовуйте підтримуваний транспорт Panel або згенеровану інтеграцію protobuf.

## NovusAgent

| Method | Interaction | Purpose |
| --- | --- | --- |
| `AgentTelemetry` | Unary | Збирає телеметрію ЦП, пам'яті та диска хоста. |
| `DockerManager` | Unary | Виконує дозволену дію життєвого циклу для контейнера середовища виконання. |
| `PtyStream` | Bidirectional stream | Ретранслює авторизовану сесію термінала. |
| `RotateMasterSecret` | Unary | Ротує секрет зв'язку між спареними Panel та Agent. |
| `PairNode` | Unary | Прив'язує неспарений Agent до одного Panel за допомогою затвердженого процесу сполучення. |
| `UnclaimNode` | Unary | Видаляє поточну прив'язку Panel. |
| `UpdateAgent` | Unary | Запитує підтримуваний робочий процес оновлення Agent. |

Фрейми `PtyStream` використовують корисне навантаження `open`, `input`, `resize`, `output`, `exit` та `error`. Початковий фрейм клієнта повинен відкрити сесію. Вибір оболонки (shell) обмежений конфігурацією Agent; браузери ніколи не отримують прямого доступу до хост-ПТК (PTY).

## InstanceService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateInstance` | Server stream | Надає середовище виконання гри, сервісу чи веб-сайту та передає прогрес потоком. |
| `ReinstallInstance` | Server stream | Перевстановлює існуючий екземпляр за допомогою поточних метаданних і параметрів матриці за замовчуванням. |
| `CheckPorts` | Unary | Перевіряє кандидатний пул портів середовища виконання. |
| `AllocatePorts` | Unary | Атомарно резервує доступний пул портів. |

## BackupService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateBackup` | Server stream | Створює архів резервної копії екземпляра та передає прогрес потоком. |
| `RestoreBackup` | Server stream | Відновлює резервну копію в екземпляр і передає прогрес потоком. |
| `DeleteBackup` | Unary | Видаляє резервну копію з вибраного адаптера. |
| `ListBackups` | Unary | Перераховує метадані резервних копій для екземпляра. |

## NovusRuntimeSurface

| Area | Methods |
| --- | --- |
| Інвентаризація хоста та середовища виконання | `HostInfo`, `RuntimeContainers` |
| VFS | `VfsList`, `VfsStat`, `VfsRead`, `VfsWrite`, `VfsDelete`, `VfsChmod`, `VfsMove`, `VfsCopy`, `VfsMkdir`, `VfsCompress`, `VfsExtract`, `VfsUploadInit`, `VfsUploadChunk`, `VfsUploadFinalize` |
| Життєвий цикл контейнера | `RuntimeContainerInspect`, `RuntimeContainerStats`, `RuntimeContainerCreate`, `RuntimeContainerRemove` |
| Файлова система контейнера | `ContainerFsList`, `ContainerFsRead`, `ContainerFsWrite`, `ContainerFsMkdir`, `ContainerFsDelete`, `ContainerFsRename`, `ContainerFsPull` |
| Метадані сертифіката веб-сайту | `WebsiteSslCertificates`, `WebsiteSslCertificate` |

`ContainerFsPull` — це серверний потік. Методи веб-сайту надають доступ до метаданих сертифікатів; випуск і поновлення сертифікатів не є методами поточного контракту `NovusRuntimeSurface`.

## Compatibility Rules

- Додавання нових полів і методів protobuf вимагає узгодженого планування випусків для Agent, кодека/клієнта Panel, тестів і релізів.
- Забороняється самостійно перейменовувати поля, змінювати номери полів, змінювати назви метаданих або змінювати порядок потоків.
- `NovusFileSystem` існує в `proto/novus_fs.proto`, але це наразі не зареєстрована поверхня сервісу. Не використовуйте його як підтримувану кінцеву точку середовища виконання, доки не буде завершено реєстрацію та документацію з сумісності.

## Errors

Обробники використовують стандартні коди стану gRPC. Клієнти повинні обробляти принаймні `InvalidArgument`, `Unauthenticated`, `PermissionDenied`, `FailedPrecondition`, `Unavailable`, `ResourceExhausted` і `Internal`, а також відображати безпечне для користувача повідомлення через Panel замість розкриття детальних даних хоста.
