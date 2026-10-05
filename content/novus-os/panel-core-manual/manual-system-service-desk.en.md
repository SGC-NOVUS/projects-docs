---
id: panel-core-manual-system-service-desk
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Service Desk
description: The Service Desk records and coordinates operational incidents. It links
  alerts, affected resources, timelines and approved notifications without exposing
  host credentials or in...
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/system/service-desk.md
managed_by: sync_private_docs
---
# Service Desk

The Service Desk records and coordinates operational incidents. It links alerts,
affected resources, timelines and approved notifications without exposing host
credentials or internal remediation procedures.

## Operator Workflow

1. Create or update an incident with impact, scope and observable symptoms.
2. Link the affected node, workload, monitoring target or operation identifier.
3. Record decisions and status changes in the incident timeline.
4. Use approved notification actions where configured.
5. Close the incident only after validating the recovery through the Panel.

## Security And Escalation

- Incident access follows the Service Desk permission policy.
- Notification integrations use protected credentials and do not reveal them in
  incident data.
- Attach correlation identifiers and timestamps instead of command output,
  secrets or host paths.
- Escalate integrity, credential and repeated availability failures to the
  authorized response team.
