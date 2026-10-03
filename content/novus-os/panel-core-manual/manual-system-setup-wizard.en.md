---
id: panel-core-manual-system-setup-wizard
cluster: novus-os
category: panel-core-manual
order: 100
status: active
version: 0.1.0
title: Setup Wizard
description: The Setup Wizard prepares a new NOVUS Panel environment through a guided,
  authenticated workflow. It validates each stage before the platform activates the
  related capability.
last_updated: '2026-10-03'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/manual/system/setup_wizard.md
managed_by: sync_private_docs
---
# Setup Wizard

The Setup Wizard prepares a new NOVUS Panel environment through a guided,
authenticated workflow. It validates each stage before the platform activates
the related capability.

## Setup Lifecycle

1. Review environment readiness and required information.
2. Complete identity and administrator setup through the wizard.
3. Configure approved platform, node and integration options.
4. Review the resulting readiness report.
5. Complete setup only after the Panel records successful validation.

## Safety Controls

- Setup requests are validated and recorded as auditable state transitions.
- Protected configuration and credentials remain outside browser-visible setup
  payloads.
- Database, key and node provisioning use idempotent platform workflows.
- Recovery and restart procedures are restricted to authorized engineering work.
