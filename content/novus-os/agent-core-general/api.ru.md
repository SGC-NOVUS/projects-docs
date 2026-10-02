---
id: agent-core-api
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Справочник по gRPC API'
description: '**Источник контракта:** proto/novus.proto и proto/novus_runtime_surface.proto.
  Номера полей, структуры сообщений и методы служб в этих файлах являются исчерпывающими.
  Эта страница представляет собой...'
last_updated: '2026-10-02'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/API.md
managed_by: sync_private_docs
---
# NOVUS Agent-Core: Справочник по gRPC API

**Источник контракта:** `proto/novus.proto` и `proto/novus_runtime_surface.proto`. Номера полей, структуры сообщений и методы сервисов в этих файлах являются авторитетными. Эта страница представляет собой справочник для безопасной навигации и не заменяет сгенерированные protobuf-клиенты.

## Транспорт и доступ

- Транспортом является gRPC поверх TLS.
- Обычные привилегированные вызовы передают метаданные `x-request-timestamp`, `x-signature` и `x-panel-uuid`.
- Agent применяет блокировку связанной Panel, проверку актуальности запроса, защиту от повторного воспроизведения (replay), лимиты запросов (rate limits) и политики аудита перед отправкой привилегированных вызовов.
- Сопряжение (pairing) и стандартные gRPC-проверки работоспособности (health checks) являются исключениями для начальной загрузки (bootstrap) и проверки активности (liveness). Не реализуйте клиент только на основе этого документа; используйте поддерживаемый транспорт Panel или сгенерированную protobuf-интеграцию.

## NovusAgent

| Метод | Взаимодействие | Назначение |
| --- | --- | --- |
| `AgentTelemetry` | Унарный (Unary) | Собирает телеметрию хоста по CPU, памяти и диску. |
| `DockerManager` | Унарный (Unary) | Выполняет разрешенное действие жизненного цикла для контейнера среды выполнения. |
| `PtyStream` | Двунаправленный поток (Bidirectional stream) | Ретранслирует авторизованную сессию терминала. |
| `RotateMasterSecret` | Унарный (Unary) | Выполняет ротацию секретного ключа между связанными Panel и Agent. |
| `PairNode` | Унарный (Unary) | Привязывает несопряженный Agent к одной Panel с использованием утвержденного процесса сопряжения. |
| `UnclaimNode` | Унарный (Unary) | Удаляет текущую привязку к Panel. |
| `UpdateAgent` | Унарный (Unary) | Запрашивает поддерживаемый рабочий процесс обновления Agent. |

Фреймы `PtyStream` используют полезную нагрузку (payloads) `open`, `input`, `resize`, `output`, `exit` и `error`. Первый фрейм клиента должен открывать сессию. Выбор оболочки (shell) ограничивается конфигурацией Agent; браузеры никогда не получают прямой доступ к host PTY.

## InstanceService

| Метод | Взаимодействие | Назначение |
| --- | --- | --- |
| `CreateInstance` | Поток сервера (Server stream) | Подготавливает игру, сервис или веб-среду выполнения и передает поток прогресса. |
| `ReinstallInstance` | Поток сервера (Server stream) | Переустанавливает существующий экземпляр, используя текущие метаданные и значения матрицы по умолчанию. |
| `CheckPorts` | Унарный (Unary) | Проверяет пул потенциальных портов среды выполнения. |
| `AllocatePorts` | Унарный (Unary) | Атомарно резервирует доступный пул портов. |

## BackupService

| Метод | Взаимодействие | Назначение |
| --- | --- | --- |
| `CreateBackup` | Поток сервера (Server stream) | Создает архив резервной копии экземпляра и передает поток прогресса. |
| `RestoreBackup` | Поток сервера (Server stream) | Восстанавливает резервную копию в экземпляр и передает поток прогресса. |
| `DeleteBackup` | Унарный (Unary) | Удаляет резервную копию из выбранного адаптера. |
| `ListBackups` | Унарный (Unary) | Перечисляет метаданные резервных копий для экземпляра. |

## NovusRuntimeSurface

| Область | Методы |
| --- | --- |
| Инвентаризация хоста и среды выполнения | `HostInfo`, `RuntimeContainers` |
| VFS | `VfsList`, `VfsStat`, `VfsRead`, `VfsWrite`, `VfsDelete`, `VfsChmod`, `VfsMove`, `VfsCopy`, `VfsMkdir`, `VfsCompress`, `VfsExtract`, `VfsUploadInit`, `VfsUploadChunk`, `VfsUploadFinalize` |
| Жизненный цикл контейнера | `RuntimeContainerInspect`, `RuntimeContainerStats`, `RuntimeContainerCreate`, `RuntimeContainerRemove` |
| Файловая система контейнера | `ContainerFsList`, `ContainerFsRead`, `ContainerFsWrite`, `ContainerFsMkdir`, `ContainerFsDelete`, `ContainerFsRename`, `ContainerFsPull` |
| Метаданные сертификатов веб-сайтов | `WebsiteSslCertificates`, `WebsiteSslCertificate` |

`ContainerFsPull` является потоком сервера (server stream). Методы веб-сайтов предоставляют метаданные сертификатов; выпуск и продление сертификатов не являются методами текущего контракта `NovusRuntimeSurface`.

## Правила совместимости

- Аддитивные protobuf-поля и методы требуют согласованного планирования для Agent, кодека/клиента Panel, тестов и релизов.
- Запрещается самостоятельно переименовывать поля, изменять номера полей, менять названия метаданных или изменять порядок потоков.
- `NovusFileSystem` существует в `proto/proto/novus_fs.proto`, но в настоящее время не является зарегистрированной поверхностью сервиса. Не используйте его в качестве поддерживаемой конечной точки среды выполнения до завершения регистрации и документации по совместимости.

## Ошибки

Обработчики используют стандартные коды состояния gRPC. Клиенты должны обрабатывать как минимум `InvalidArgument`, `Unauthenticated`, `PermissionDenied`, `FailedPrecondition`, `Unavailable`, `ResourceExhausted` и `Internal`, а также должны отображать безопасное для пользователя сообщение через Panel, вместо того чтобы раскрывать исходные детали хоста.
