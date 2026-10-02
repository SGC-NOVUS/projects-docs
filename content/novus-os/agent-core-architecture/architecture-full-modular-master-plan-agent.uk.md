---
id: agent-core-architecture-full-modular-master-plan-agent
cluster: novus-os
category: agent-core-architecture
order: 100
status: active
version: 0.1.0
title: ПОВНИЙ МОДУЛЬНИЙ ГЕНПЛАН – AGENT CORE (КАНОНІЧНИЙ SSoT)
description: 'Статус: ЗАВЕРШЕНО ТА ЗАБЛОКОВАНО (Базова версія v0.2.0, 2026-09-25)'
last_updated: '2026-10-02'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/architecture/FULL_MODULAR_MASTER_PLAN_AGENT.md
managed_by: sync_private_docs
---
них шляхів оркестрації InstanceLifecycle.`
        *   `  - BackupOrchestration application service introduced under internal/modules/backup_orchestration/application.` -> `  - Впроваджено прикладний сервіс BackupOrchestration у internal/modules/backup_orchestration/application.`
        *   `  - CreateBackup, RestoreBackup, DeleteBackup, and ListBackups orchestration moved out of grpc transport into module application service.` -> `  - Оркестрацію CreateBackup, RestoreBackup, DeleteBackup та ListBackups перенесено з grpc-транспорту до прикладного сервісу модуля.`
        *   `  - gRPC BackupService transport now delegates these paths while preserving stream envelopes and status mappings.` -> `  - gRPC-транспорт BackupService тепер делегує ці шляхи, зберігаючи потокові оболонки та мапінг статусів.`
        *   `  - Focused module unit tests added for extracted BackupOrchestration paths.` -> `  - Додано цільові модульні юніт-тести для виділених шляхів BackupOrchestration.`
        *   `- C4 delivered:` -> `- C4 виконано:`
        *   `  - WebSocket console orchestration moved into internal/modules/transport_websocket_console/application/service.go.` -> `  - Оркестрацію консолі WebSocket перенесено до internal/modules/transport_websocket_console/application/service.go.`
        *   `  - gRPC
