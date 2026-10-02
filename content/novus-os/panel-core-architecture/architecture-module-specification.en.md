---
id: panel-core-architecture-module-specification
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: MODULE SPECIFICATION
description: 'Status: normative Owner: Panel Core Engineering Scope: panel-core module
  architecture Last updated: 2026-09-24 Anchors: AGENTS.md, ECOSYSTEM_MANIFEST.md,
  Master Plan WS-D'
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/MODULE_SPECIFICATION.md
managed_by: sync_private_docs
---
# MODULE SPECIFICATION

Status: normative
Owner: Panel Core Engineering
Scope: panel-core module architecture
Last updated: 2026-09-24
Anchors: [AGENTS.md](../../AGENTS.md), [ECOSYSTEM_MANIFEST.md](../../ECOSYSTEM_MANIFEST.md), [Master Plan WS-D](../dev/MASTER_PLAN_PANEL_ENTERPRISE_AAA_2026-09-23.md)

## 1. Mission and Fleet Scope

This specification is the Golden Standard for designing, auditing, and refactoring modules in NOVUS-OS Panel.

NOVUS-OS is an enterprise multi-node control plane for:

1. Virtual infrastructure (VPS and cloud nodes).
2. Physical infrastructure (bare-metal servers).
3. Runtime orchestration and lifecycle management.
4. Service monitoring and host/service health observability.
5. ServiceDesk and incident management workflows.
6. Websites (Nginx, PHP-FPM, SSL lifecycle).
7. Database isolation and tenant database operations.
8. Backups and platform operations.

Topology model:

1. Panel is the control-plane orchestrator (policy, intent, state, API contract).
2. Agent is the execution-plane daemon on managed nodes.
3. Installer is bootstrap-only and does not own runtime orchestration.

Supported deployment profiles:

1. Bare-metal fleet.
2. VPS/KVM fleet.
3. Cloud VM fleet.
4. Hybrid fleet (mixed node classes under one control plane).

## 2. Architectural Invariants (Zero Deviation)

These rules are mandatory for all new modules and all refactors.

1. No framework facade layer is allowed for module runtime behavior.
2. Service registration and resolution are executed via [app/Support/Container.php](../../app/Support/Container.php).
3. Route composition is executed via custom router contracts in [app/Http/Router.php](../../app/Http/Router.php) and [routes/api.php](../../routes/api.php).
4. Control-plane persistence uses PostgreSQL 18 through native PDO connections `os`, `id`, and `sd`.
5. Data-plane tenant DB operations use MariaDB 11.4+ through PDO connection `payload`.
6. Direct host execution from panel controllers/services is prohibited (`shell_exec`, `exec`, `proc_open`, `passthru`, `system`).
7. Host and runtime operations are allowed only through typed Agent transport contracts, using [app/Services/Agent/NovusAgentClient.php](../../app/Services/Agent/NovusAgentClient.php).
8. Vue module styling must use Tailwind tokenized semantic classes and theme variables from [config/themes.php](../../config/themes.php).
9. `<style scoped>` and inline `style="..."` in Vue templates are prohibited for module surfaces.
10. i18n literals in Vue templates are prohibited; module text must come from `resources/locales/{ru,en,uk}` dictionaries.

## 3. Backend Domain Blueprint (app/Modules/<Domain>/)

### 3.1 Required directory layout

Each backend domain module must include the following directories and role split:

1. `Http/` for container-registered endpoint handlers/controllers.
2. `Services/` for domain business logic and orchestration.
3. `Providers/` for deterministic container registration files.
4. `Routes/` for domain route manifests.

Minimal skeleton:

```text
app/Modules/<Domain>/
├── Http/
│   └── controllers.php
├── Services/
│   └── runtime_services.php
├── Providers/
│   ├── <domain>_core.php
│   └── <domain>_http.php
└── Routes/
    └── api.php
```

### 3.2 Http layer requirements

1. API controllers must inherit from `App\Controllers\Api\ApiController`.
2. Success responses must use deterministic envelope contracts (controller `ok` helper and/or `Response::json` with `{ ok: true, data: ... }`).
3. Failure responses must use deterministic envelope contracts via controller fail helpers (canonical shape: `{ ok: false, error: { code, message } }` with compatibility fields when required by current migration policy).
4. Free-form string `error` payloads are prohibited for non-protocol endpoints.
5. Route handlers must be thin adapters: input normalization, permission gate, service call, deterministic response mapping.

### 3.3 Protocol Exceptions Policy (OAuth 2.0 / OIDC)

The deterministic envelope rule has an explicit protocol exception:

1. OAuth 2.0 / OIDC protocol endpoints (for example [app/Controllers/Api/OidcProtocolController.php](../../app/Controllers/Api/OidcProtocolController.php)) must follow RFC 6749-compatible error shape.
2. Allowed protocol error payload format:

```json
{
  "error": "invalid_request",
  "error_description": "Missing parameter: client_id"
}
```

3. Protocol endpoints under this exception must be covered by dedicated protocol tests proving RFC-compatible behavior.
4. This exception is narrow and must not be reused by non-protocol panel APIs.

### 3.4 Services layer requirements

1. Services hold business logic, state transitions, and transaction boundaries.
2. Services must not produce raw HTTP output objects.
3. Services must not call host commands directly.
4. Runtime and host mutations must be delegated to `NovusAgentClient` typed methods.
5. Input/output types must be deterministic and auditable.

### 3.5 Providers and bootstrap wiring

1. Module container registrations must be deterministic and file-based.
2. Registrations must be compatible with [app/Support/Container.php](../../app/Support/Container.php).
3. Module provider files must be loaded through orchestrated bootstrap order (see [app/Modules/SystemCore/Providers/bootstrap_orchestrator.php](../../app/Modules/SystemCore/Providers/bootstrap_orchestrator.php)).
4. Provider registration order must be append-only unless an explicit migration plan states otherwise.

### 3.6 Routes and permission enforcement

1. Every module must own a domain-isolated route manifest in `Routes/api.php`.
2. Module route manifests must be included by [routes/api.php](../../routes/api.php), not embedded ad-hoc in unrelated modules.
3. Permission policy must be enforced for each mutable endpoint.
4. Required permission naming contract: `platform.<domain>.<action>`.
5. Permission enforcement must be applied by permission middleware contract and/or ApiController guard helpers, with deterministic deny behavior.

## 4. Frontend Domain Blueprint (resources/js/modules/<Domain>/)

### 4.1 Required directory layout

```text
resources/js/modules/<Domain>/
├── views/
├── components/
├── api/
├── stores/
└── locales/
```

If a legacy domain does not yet contain all directories, migration backlog must track convergence to this layout.

### 4.2 Vue SFC and UI standards

1. Vue 3 SFC with script setup is the default authoring mode.
2. `<style scoped>` is prohibited.
3. Inline style attributes are prohibited for module surfaces.
4. Tokenized Tailwind classes and shared theme variables are mandatory.
5. Reuse shared windowing and shell components for modal/window behavior (for example [resources/js/modules/Common/components/DesktopWindowWrapper.vue](../../resources/js/modules/Common/components/DesktopWindowWrapper.vue)).
6. Hardcoded user-visible strings in templates are prohibited.

### 4.3 Frontend transport typing

1. Each module API adapter (`api/<domain>Api.ts`) must use unified typed transport (`novusFetch<T>` target defined by WS-D.2).
2. API response typing must model deterministic server contracts.
3. Auth/session error handling must be centralized and non-looping.
4. Module-level transport wrappers that bypass unified error mapping are prohibited.

## 5. Data-Plane vs Control-Plane Access Rules

### 5.1 Control-plane database usage

Use PostgreSQL control-plane connections (`os`, `id`, `sd`) for panel state and identity/service-desk state.

Example (control-plane):

```php
$os = $this->connections->connection('os');
$id = $this->connections->connection('id');
$sd = $this->connections->connection('sd');
```

### 5.2 Data-plane database usage

Use payload MariaDB connection only for tenant/user databases:

```php
$payload = $this->connections->connection('payload');
```

This boundary is mandatory and must not be bypassed by direct DSN construction in module logic.

### 5.3 Typed query helpers and identity

1. Use [app/Services/Database/DatabaseHelper.php](../../app/Services/Database/DatabaseHelper.php) for parameter normalization and JSON/JSONB-safe mapping.
2. Use UUIDv7 IDs through [app/Support/UuidV7.php](../../app/Support/UuidV7.php) for entity/request correlation where module contracts require generated identifiers.
3. Module logic must keep control-plane and data-plane SQL concerns separated by explicit connection intent.

## 6. Host Orchestration and Transport Rules

### 6.1 Allowed host operation path

1. Panel receives intent through authenticated API endpoint.
2. Panel validates IAM/OIM permissions.
3. Panel maps intent to typed Agent RPC through `NovusAgentClient`.
4. Agent executes host-local operation and returns typed result.
5. Panel maps result to deterministic API response contract.

### 6.2 Prohibited patterns in panel modules

The following are prohibited inside panel controllers/services:

1. `shell_exec`, `exec`, `proc_open`, `passthru`, `system`.
2. Direct `docker.sock` access.
3. Local PTY ownership in panel runtime.
4. Root-level command orchestration from panel HTTP paths.

Compatibility debt found in legacy surfaces is not a precedent for new code.

## 7. Contract Enforcement and Quality Gates

### 7.1 Validation gates

WS-D quality enforcement is based on existing and planned checks:

1. docs link integrity checks.
2. quality fast pipeline checks.
3. module contract guard script: [tools/quality/module_contract_check.php](../../tools/quality/module_contract_check.php).

### 7.2 CI fail criteria

A module change must fail CI if any condition is true:

1. Non-protocol API endpoint returns non-deterministic failure shape.
2. Disallowed host-exec pattern is detected in module controllers/services.
3. Module Vue templates contain `<style scoped>` or inline style attributes.
4. Module Vue templates include hardcoded user-facing literals instead of i18n keys.
5. Route surface changes are not aligned with domain route manifests and permission policy.

### 7.3 Required checks for WS-D.1 and later

Run and keep green:

1. `php tools/quality/docs_link_check.php`
2. `npm run quality:fast`

## 8. Golden References and Audit Baseline

### 8.1 Backend golden reference

Reference module: [app/Modules/Databases](../../app/Modules/Databases)

Audit expectations:

1. Explicit connection boundaries.
2. Container-based registration.
3. Domain route manifest ownership.
4. Deterministic API contract mapping.

### 8.2 Frontend golden reference

Reference module: [resources/js/modules/Services](../../resources/js/modules/Services)

Audit expectations:

1. Component isolation by domain.
2. Tailwind token usage and theme alignment.
3. Shared shell/window integration.
4. Progressive convergence to full module layout contract.

## 9. Adoption Procedure

1. New module creation must start from this specification.
2. Existing module refactor plans must cite this specification in task scope.
3. Any exception requires explicit architecture decision record in `docs/dev` with owner and expiry.
4. If this document and any older guide conflict, this document is authoritative for module architecture.
