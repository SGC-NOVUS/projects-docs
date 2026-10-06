---
id: agent-core-api
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Справочник по gRPC API'
description: '**Источник контракта:** proto/novus.proto и proto/novus_runtime_surface.proto.
  Номера полей, структуры сообщений и методы сервисов в этих файлах являются авторитетными.
  Эта страница представляет собой...'
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/API.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core: gRPC API Reference

**Contract source:** `proto/novus.proto` и `proto/novus_runtime_surface.proto`. Номера полей, структуры сообщений и методы сервисов в этих файлах являются авторитетными. Эта страница представляет собой справочник по безопасной навигации, а не замену сгенерированным клиентам protobuf.

## Transport And Access

- Транспортом является gRPC поверх TLS.
- Обычные привилегированные вызовы содержат метаданные `x-request-timestamp`, `x-signature` и `x-panel-uuid`.
- Агент применяет блокировку связанной Control-Plane/Panel, проверку актуальности запроса, защиту от повторного воспроизведения (Replay Guard), ограничения частоты запросов и политику аудита перед отправкой привилегированных вызовов.
- Сопряжение и стандартные проверки работоспособности gRPC являются исключениями для инициализации и проверки активности (liveness). Не реализуйте клиент только на основе этого документа; используйте поддерживаемый транспорт Panel или сгенерированную интеграцию protobuf.

## NovusAgent

| Method | Interaction | Purpose |
| --- | --- | --- |
| `AgentTelemetry` | Unary | Собирает телеметрию хоста по CPU, памяти и диску. |
| `DockerManager` | Unary | Выполняет разрешенное действие жизненного цикла для контейнера среды выполнения. |
| `PtyStream` | Bidirectional stream | Передает авторизованную сессию терминала. |
| `RotateMasterSecret` | Unary | Выполняет ротацию секретной пары Panel-to-Agent. |
| `PairNode` | Unary | Привязывает несопряженный Agent к одной Panel с использованием утвержденного процесса сопряжения. |
| `UnclaimNode` | Unary | Удаляет текущую привязку к Panel. |
| `UpdateAgent` | Unary | Запрашивает поддерживаемый рабочий процесс обновления Agent. |

Фреймы `PtyStream` используют полезную нагрузку (payloads) `open`, `input`, `resize`, `output`, `exit` и `error`. Первый фрейм клиента должен открывать сессию. Выбор оболочки ограничивается конфигурацией Agent; браузеры никогда не получают прямой доступ к PTY хоста.

## InstanceService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateInstance` | Server stream | Выделяет ресурсы для игрового, сервисного или веб-окружения и передает поток данных о прогрессе. |
| `ReinstallInstance` | Server stream | Переустанавливает существующий экземпляр, используя текущие метаданные и значения матрицы по умолчанию. |
| `CheckPorts` | Unary | Проверяет пул потенциальных портов среды выполнения. |
| `AllocatePorts` | Unary | Атомарно резервирует доступный пул портов. |

## BackupService

| Method | Interaction | Purpose |
| --- | --- | --- |
| `CreateBackup` | Server stream | Создает архив резервной копии экземпляра и передает поток данных о прогрессе. |
| `RestoreBackup` | Server stream | Восстанавливает резервную копию в экземпляр и передает поток данных о прогрессе. |
| `DeleteBackup` | Unary | Удаляет резервную копию из выбранного адаптера. |
| `ListBackups` | Unary | Выводит список метаданных резервных копий для экземпляра. |

## NovusRuntimeSurface

| Area | Methods |
| --- | --- |
| Host and runtime inventory | `HostInfo`, `RuntimeContainers` |
| VFS | `VfsList`, `VfsStat`, `VfsRead`, `VfsWrite`, `VfsDelete`, `VfsChmod`, `VfsMove`, `VfsCopy`, `VfsMkdir`, `VfsCompress`, `VfsExtract`, `VfsUploadInit`, `VfsUploadChunk`, `VfsUploadFinalize` |
| Container lifecycle | `RuntimeContainerInspect`, `RuntimeContainerStats`, `RuntimeContainerCreate`, `RuntimeContainerRemove` |
| Container filesystem | `ContainerFsList`, `ContainerFsRead`, `ContainerFsWrite`, `ContainerFsMkdir`, `ContainerFsDelete`, `ContainerFsRename`, `ContainerFsPull` |
| Website certificate metadata | `WebsiteSslCertificates`, `WebsiteSslCertificate` |

`ContainerFsPull` является серверным потоком. Методы веб-сайтов предоставляют метаданные сертификатов; выпуск и продление сертификатов не являются частью текущего контракта `NovusRuntimeSurface`.

## Правила совместимости

- Аддитивные protobuf-поля и методы требуют согласованного планирования для Agent, кодека/клиента Panel, тестов и релиза.
- Запрещается самостоятельно переименовывать поля, изменять номера полей, менять названия метаданных или нарушать порядок потоков (streams).
- `NovusFileSystem` присутствует в `proto/novus_fs.proto`, но на данный момент не является зарегистрированной поверхностью сервиса. Не используйте его в качестве поддерживаемой среды выполнения (runtime-эндпоинта) до завершения регистрации и подготовки документации по совместимости.

## Ошибки

Обработчики используют стандартные коды статуса gRPC. Клиенты должны обрабатывать как минимум `InvalidArgument`, `Unauthenticated`, `PermissionDenied`, `FailedPrecondition`, `Unavailable`, `ResourceExhausted` и `Internal`, а также выводить безопасное для пользователя сообщение через Panel, не раскрывая исходные детали хоста.
