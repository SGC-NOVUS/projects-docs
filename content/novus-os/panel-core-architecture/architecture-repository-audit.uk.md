---
id: panel-core-architecture-repository-audit
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: Аudit поверхні репозиторію
description: '- Структура репозиторію та поверхня модулів - Інвентаризація REST-маршрутів
  (routes/api.php) - Інвентаризація сервісів / контролерів / воркерів - Поверхня фронтенду
  (resources/js) - Зони високої кон...'
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/repository_audit.md
managed_by: sync_private_docs
---
# Аудит поверхні репозиторію

## Обсяг
- Структура репозиторію та поверхня модулів
- Інвентаризація REST-маршрутів (`routes/api.php`)
- Інвентаризація сервісів/контролерів/воркерів
- Поверхня фронтенду (`resources/js`)
- Гарячі точки з високою концентрацією та шари сумісності

## Поточні метрики
| Метрика | Значення |
|---|---:|
| Всього маршрутів (метод+шлях) | 1 |
| Унікальні REST-шляхи | 1 |
| Класи сервісів (`app/Services`) | 213 |
| Класи контролерів (`app/Controllers`) | 52 |
| Класи воркерів (`app/Workers`) | 1 |
| Файли документації Markdown (`docs`) | 106 |
| Обгортки сумісності (`tools/*.php`) | 18 |

## Топ файлів контролерів за кількістю рядків коду (LOC)
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

## Основні файли служб за кількістю рядків коду (LOC)
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

## Основні фронтенд-файли за розміром
| Файл | Розмір |
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

## Структурні зауваження
- Основне навантаження щодо декомпозиції залишається у найбільших файлах контролерів та сервісів, перелічених вище.
- Складовані скрипти тепер розміщуються в каталозі `tools/{audit,daemons,maintenance,migrations,openapi,quality}`, тоді як `tools/*.php` зберігає обгортки сумісності для наявних операційних точок входу.
- Відхилення від відкритої архітектури та розбіжності в документації відстежуються у внутрішній технічній документації та виключені з поверхні публічної документації.

## Рекомендовані подальші кроки
- Продовжувати зменшення гарячих точок контролерів/сервісів шляхом перенесення оркестрації, шляхів запитів та шляхів мутацій до більш вузьких сервісів.
- Зберігати згенеровану документацію (`repository_audit.md`, `services_full_inventory.md`) в тому ж наборі змін (change-set), що й зміни поверхні сервісів або маршрутів.
