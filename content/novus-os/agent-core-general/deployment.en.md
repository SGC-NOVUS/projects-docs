---
id: agent-core-deployment
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: NOVUS Agent Deployment
description: NOVUS Agent is deployed by the approved NOVUS installation or node-management
  workflow. Operators pair and monitor nodes through the Panel; they do not apply
  host service config...
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/DEPLOYMENT.md
managed_by: sync_private_docs
---
# NOVUS Agent Deployment

NOVUS Agent is deployed by the approved NOVUS installation or node-management
workflow. Operators pair and monitor nodes through the Panel; they do not apply
host service configuration or credentials directly.

## Deployment Lifecycle

1. Confirm that the target host meets the supported platform requirements.
2. Use the approved installer or Panel node workflow to deploy the release.
3. Pair the node through the authenticated Panel workflow.
4. Review node health and transport status in the Panel.
5. Record release, pairing and validation results in change control.

## Security Model

- Agent transport uses authenticated, encrypted communication.
- Installation secrets and key material remain under the protected host
  configuration boundary.
- The deployment process verifies the configured release before activation.
- Operators use Panel health signals and incident workflows for failures.

## Troubleshooting

Retain the node identity, pairing state and displayed health error. Retry only a
safe action offered by the Panel or installer. Escalate unavailable transport,
credential or certificate failures to the authorized platform team.

Build, service configuration and recovery procedures are restricted to the
internal engineering procedure.
