---
id: panel-core-troubleshooting
cluster: novus-os
category: panel-core-general
order: 100
status: active
version: 0.1.0
title: Troubleshooting Hub
description: This guide helps operators collect useful context without bypassing NOVUS-OS
  security boundaries. Use Panel status, audit records and the approved incident workflow
  for producti...
last_updated: '2026-10-02'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/TROUBLESHOOTING.md
managed_by: sync_private_docs
translation_status: pending
---
# Troubleshooting Hub

This guide helps operators collect useful context without bypassing NOVUS-OS security boundaries. Use Panel status, audit records and the approved incident workflow for production issues.

## Panel Is Unavailable Or Incomplete

Record the affected URL, time, browser error and visible Panel state. Confirm whether the issue affects one user or multiple users. Do not modify deployed files, service configuration or caches directly; escalate the evidence to the platform response team.

## Authentication Or Access Is Denied

Confirm that the correct account, role and current authentication method are in use. Ask an authorized access administrator to review the relevant account, session and policy state. Do not share credentials or recovery material in a ticket.

## A Managed Operation Failed

Keep the operation or correlation identifier, selected resource, request time and reported error. Check node and workload status in the Panel. Use a retry only when the UI offers a safe retry action; otherwise create or update an incident.

## Documentation Or Contract Drift

For development work, rebuild the documentation snapshot and run the documented quality gates. API changes must be reflected in the canonical OpenAPI reference and the human-readable endpoint inventory before release.

## Related Guides

- [Platform Operations](manual/system/services.md)
- [System Security](manual/system/security.md)
- [Files And Storage](manual/infrastructure/vfs.md)
- [Databases](manual/resources/databases.md)
- [Backups](manual/resources/backups.md)
- [REST Endpoints](api-reference/rest_endpoints.md)

Detailed diagnostics, migration recovery and release procedures are restricted to `docs/dev` for authorized engineering work.
