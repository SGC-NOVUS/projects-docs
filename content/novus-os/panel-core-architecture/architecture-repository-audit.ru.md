---
id: panel-core-architecture-repository-audit
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: Аудит поверхности репозитория
description: '- Структура репозитория и поверхность модулей - Реестр REST-маршрутов
  (routes/api.php) - Реестр сервисов / контроллеров / воркеров - Поверхность фронтенда
  (resources/js) - Зоны высокой концентрац...'
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/repository_audit.md
managed_by: sync_private_docs
---
# Аудит поверхности репозитория

## Область охвата
- Структура репозитория и поверхность модулей
- Инвентаризация REST-маршрутов (`routes/api.php`)
- Инвентаризация сервисов/контроллеров/воркеров
- Поверхность фронтенда (`resources/js`)
- Горячие точки с высокой концентрацией кода и уровни совместимости

## Текущие метрики
| Метрика | Значение |
|---|---:|
| Всего маршрутов (метод+путь) | 1 |
| Уникальные REST-пути | 1 |
| Классы сервисов (`app/Services`) | 213 |
| Классы контроллеров (`app/Controllers`) | 52 |
| Классы воркеров (`app/Workers`) | 1 |
| Файлы документации Markdown (`docs`) | 106 |
| Обертки совместимости (`tools/*.php`) | 18 |

## Топовые файлы контроллеров по количеству строк кода (LOC)
| Файл | LOC |
|---|---:|
| `app/Controllers/Api/InstancesController.php` | 1784 |
| `app/Controllers/Api/WebsitesController.php` | 818 |
| `app/Controllers/Api/MatricesController.php` | 703 |
| `app/Controllers/Api/BackupsController.php` | 625 |
| `app/Controllers/Api/VfsController.php` | 593 |
| `app/Controllers/Api/DashboardController.php` | 593 |
| `app/Controllers/Api/AgentGatewayController.php` | 592 |
| `app/Controllers/Api/ProfileController.php` | 582 |
| `app/Controllers/Api/BotsController.php` | 580 |
| `app/Controllers/Api/DatabasesController.php` | 567 |

## Основные файлы сервисов по количеству строк кода (LOC)
| Файл | LOC |
|---|---:|
| `app/Services/Infrastructure/NovusAgent/NovusProtobufCodec.php` | 3221 |
| `app/Services/Infrastructure/MatrixSyncService.php` | 2356 |
| `app/Services/Infrastructure/NovusAgent/VfsOperationsTrait.php` | 1505 |
| `app/Services/Runtime/InstanceService.php` | 1475 |
| `app/Services/Infrastructure/NovusAgent/NovusAgentDirectDriver.php` | 1433 |
| `app/Services/Security/SecretsManagerService.php` | 1331 |
| `app/Services/Identity/ProfileService.php` | 1302 |
| `app/Services/Runtime/SchedulerService.php` | 1224 |
| `app/Services/Database/DatabaseMigrationService.php` | 1177 |
| `app/Services/Monitoring/InfluxTelemetryService.php` | 1111 |

## Основные фронтенд-файлы по размеру
| Файл | Размер |
|---|---:|
| `resources/js/modules/Matrices/views/MatricesIndex.vue` | 167.8 KB |
| `resources/js/modules/Profile/views/ProfilePanelFeatureModule.vue` | 135.3 KB |
| `resources/js/modules/Files/views/FileManagerFeatureModule.vue` | 132.6 KB |
| `resources/js/modules/Bots/views/BotsPanelFeatureModule.vue` | 132.1 KB |
| `resources/js/modules/Websites/views/WebsitesIndex.vue` | 130.3 KB |
| `resources/js/modules/Settings/views/SettingsPanelFeatureModule.vue` | 127.0 KB |
| `resources/js/modules/Users/views/UsersPanelFeatureModule.vue` | 125.0 KB |
| `resources/js/dashboard.js` | 116.9 KB |
| `resources/js/modules/Services/components/InstancesPanelRuntimeCoreFeatureModule.vue` | 75.6 KB |
| `resources/js/modules/Nodes/views/NodesIndex.vue` | 72.8 KB |

## Структурные замечания
- Основное давление декомпозиции по-прежнему сосредоточено в крупнейших файлах контроллеров и сервисов, перечисленных выше.
- Категоризированные скрипты теперь находятся в директории `tools/{audit,daemons,maintenance,migrations,openapi,quality}`, в то время как `tools/*.php` сохраняет обертки совместимости для существующих операционных точек входа.
- Отклонения от открытой архитектуры и расхождения в документации отслеживаются во внутренней инженерной документации и исключены из публичной документации.

## Рекомендуемые дальнейшие шаги
- Продолжайте уменьшать «горячие точки» в контроллерах и сервисах, перенося оркестрацию, пути запросов и пути мутаций в более специализированные сервисы.
- Храните сгенерированную документацию (`repository_audit.md`, `services_full_inventory.md`) в том же наборе изменений (change-set), что и изменения поверхности сервисов или маршрутов.
