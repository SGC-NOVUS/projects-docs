---
id: panel-core-architecture-repository-audit
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: Repository Surface Audit
description: '- Repository structure and module surface - REST route inventory (routes/api.php)
  - Service/Controller/Worker inventory - Frontend surface (resources/js) - High-concentration
  ho...'
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/repository_audit.md
managed_by: sync_private_docs
---
# Repository Surface Audit

## Scope
- Repository structure and module surface
- REST route inventory (`routes/api.php`)
- Service/Controller/Worker inventory
- Frontend surface (`resources/js`)
- High-concentration hotspots and compatibility layers

## Current Metrics
| Metric | Value |
|---|---:|
| Total routes (method+path) | 1 |
| Unique REST paths | 1 |
| Service classes (`app/Services`) | 213 |
| Controller classes (`app/Controllers`) | 52 |
| Worker classes (`app/Workers`) | 1 |
| Markdown docs files (`docs`) | 106 |
| Compatibility wrappers (`tools/*.php`) | 18 |

## Top Controller Files by LOC
| File | LOC |
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

## Top Service Files by LOC
| File | LOC |
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

## Top Frontend Files by Size
| File | Size |
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

## Structural Notes
- Primary decomposition pressure remains in the largest controller and service files listed above.
- Categorized scripts now live under `tools/{audit,daemons,maintenance,migrations,openapi,quality}`, while `tools/*.php` keeps compatibility wrappers for existing operational entrypoints.
- Open architecture deviations and documentation drift are tracked in internal engineering documentation and are excluded from the public documentation surface.

## Suggested Follow-up
- Continue shrinking controller/service hotspots by moving orchestration, query-paths, and mutation-paths into narrower services.
- Keep generated docs (`repository_audit.md`, `services_full_inventory.md`) in the same change-set as service or route surface changes.
