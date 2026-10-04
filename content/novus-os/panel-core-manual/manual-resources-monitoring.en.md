---
id: panel-core-manual-resources-monitoring
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Monitoring
description: The Monitoring workspace manages approved health targets, probes, alerts
  and status views for NOVUS-OS resources.
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/resources/monitoring.md
managed_by: sync_private_docs
---
# Monitoring

The Monitoring workspace manages approved health targets, probes, alerts and
status views for NOVUS-OS resources.

## Operator Workflow

1. Create or select a monitored target in the Panel.
2. Configure the approved probe type, threshold and notification policy.
3. Review history, current state and any associated incident.
4. Acknowledge or resolve incidents through the Service Desk workflow.
5. Adjust retention or notification settings only through authorized Panel
   actions.

## Safety Controls

- Targets and probes are validated before activation.
- Alert changes require the monitoring-management permission.
- Notification credentials are stored by the protected integration owner and
  are never displayed in monitoring results.
- Automated monitoring work runs under the platform scheduler, not operator
  host commands.

## Troubleshooting

Keep the target, probe result and incident identifier when a check fails.
Review node and integration health in the Panel, then escalate repeated delivery
or telemetry failures through the incident workflow.
