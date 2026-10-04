---
id: panel-core-architecture-vue-email-module-plan
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: Vue Email Module Plan (Panel-Core)
description: 'Add a first-class email template module for NOVUS-OS with: - theme-aware
  HTML email generation, - versioned template storage, - UI editing and preview, -
  safe test-send and prod...'
last_updated: '2026-10-04'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/vue_email_module_plan.md
managed_by: sync_private_docs
---
# Vue Email Module Plan (Panel-Core)

## Goal
Add a first-class email template module for NOVUS-OS with:
- theme-aware HTML email generation,
- versioned template storage,
- UI editing and preview,
- safe test-send and production delivery pipelines.

## Feasibility
This is realistic and technically straightforward in phased rollout.
Main complexity is not rendering, but template governance (versioning, i18n, approvals, and delivery safety).

## Recommended Stack
- `vue-email` for authoring templates as Vue components.
- `@vue-email/components` for email-safe building blocks.
- `@vue-email/render` for server-side HTML rendering.
- Optional visual editor layer:
  - `vue-email-editor` (Unlayer wrapper) for drag-and-drop UX.
  - Keep code-template mode as canonical source to avoid lock-in.

## Proposed Architecture

### 1) Backend (PHP control-plane)
- New module: `NotificationsEmail`.
- Storage tables:
  - `panel_email_templates` (id, key, locale, schema_version, status, created_by, updated_by, timestamps).
  - `panel_email_template_revisions` (template_id, revision, source_json, compiled_html, subject, checksum, created_by, created_at).
  - `panel_email_dispatch_log` (template_key, recipient, transport, status, provider_id, error_code, sent_at).
- Services:
  - Template registry service.
  - Renderer bridge service (Node sidecar or CLI call) to render Vue Email to HTML.
  - Test send service with sandbox recipient allowlist.

### 2) Frontend (Vue modules)
- New module: `resources/js/modules/NotificationsEmail`.
- Views:
  - Template catalog,
  - Template editor,
  - Revision history and diff,
  - Live preview (desktop + mobile width presets),
  - Test-send panel.
- Theme integration:
  - consume only `var(--sgc-*)` and `var(--novus-*)` tokens from `config/themes.php` contract,
  - export a deterministic email token subset (no runtime-only effects like blur/backdrop).

### 3) Rendering and Delivery
- Render path:
  1. User edits Vue Email template.
  2. Template compiles to HTML in isolated renderer runtime.
  3. HTML snapshot stored with immutable revision.
- Delivery transports:
  - SMTP provider adapter (first phase),
  - API providers later (Mailgun/SES/Postmark).

## Security and Compliance
- Strict sanitization and blocked tags/attributes for unsafe HTML.
- No inline secrets in templates.
- Per-template RBAC (`platform.notifications.email.read/manage/send`).
- Full audit trail for publish, rollback, and send events.

## Incremental Delivery Plan

### Phase 1 (Low risk)
- Add backend schema + API for template CRUD and revisions.
- Add code-based template editor (no drag-and-drop).
- Add preview and sandbox test-send.

### Phase 2
- Add visual editor (`vue-email-editor`) behind feature flag.
- Add merge-tag builder and validation.

### Phase 3
- Add workflow automation (event-triggered emails),
- Add A/B template variants and delivery metrics.

## Known Risks
- Drag-and-drop editor vendor coupling.
- HTML/email client compatibility drift.
- Template migration complexity when introducing breaking schema changes.

## Decision
Proceed with Phase 1 first, code-template canonical mode, then add visual editor as optional layer.
