---
id: panel-core-contributing
cluster: novus-os
category: panel-core-general
order: 100
status: active
version: 0.1.0
title: 'Contributing: Documentation and Contracts'
description: Rules for keeping docs/ and API contracts synchronized with code.
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/CONTRIBUTING.md
managed_by: sync_private_docs
---
# Contributing: Documentation and Contracts

Rules for keeping `docs/` and API contracts synchronized with code.

## 1. Baseline

- One document, one clear scope.
- Do not store temporary reports in active module docs.
- Keep internal links relative and valid.
- English is the canonical language for architecture/API/security docs.

## 2. Mandatory Updates

- If `routes/api.php` changes, regenerate and commit:
  - `docs/api-reference/openapi_3.1.yaml`
  - `docs/api/openapi.json`
  - `docs/api/openapi.yaml`
  - `docs/api/openapi.public.yaml`
  - route/spec sync pass via `tools/quality/route_spec_sync.php`
- If `app/Services/*` changes or a new public service is added, regenerate and commit:
  - `docs/functions/services_full_inventory.md`
- If navigation, route ownership or mounted Vue surfaces change, update:
  - `docs/dev/product_surface_map.md`
  - related module docs in `docs/manual/`
- If module behavior changes, update related file in `docs/manual/`.
- If UI or i18n policy changes, update `docs/dev/style_contract.md`, `docs/dev/i18n_policy.md` и связанные документы в `docs/dev/`.
- If new docs section is added, update `docs/README.md`.
- If docs content changes, regenerate and commit:
  - `docs/project_documentation_unified.md`
- Temporary plans and working notes belong in `docs/dev/tasks/`, `docs/dev/cleanup/` or dated files in `docs/dev/`.
- Historical audits, timezone notes and legacy contracts must be placed in `docs/dev/archive/`.

## 3. Required Checks Before Merge

```bash
php tools/openapi/generate_openapi.php
php tools/audit/services_inventory.php
npm run docs:unified
php tools/quality/route_spec_sync.php
php tools/quality/openapi_split_guard.php
node tools/quality/docs_contract_coverage_check.mjs
node tools/quality/i18n_parity.mjs --strict
node tools/quality/no_local_vue_styles.mjs
php tools/quality/docs_link_check.php
bash tools/quality/run_fast_gates.sh
```

Before release or large refactors, additionally run `bash tools/quality/run_gates.sh`.

`tools/quality/run_gates.sh` regenerates these artifacts and, in git-aware environments, fails if generated files were not committed.

## 4. Style Rules

- Keep wording concise and implementation-oriented.
- Use stable terminology for modules, endpoints, permissions, and events.
- Separate factual behavior from historical notes.
- Use code blocks for commands and payload examples.
- Prefer updating existing docs over creating parallel documents with overlapping ownership.
