---
id: panel-core-architecture-ecosystem-manifest
cluster: novus-os
category: panel-core-architecture
order: 100
status: active
version: 0.1.0
title: NOVUS-OS Ecosystem Manifest
description: '**Status:** normative cross-repository architecture contract **Scope:**
  panel-core, agent-core, and installer **Canonical source:** this document is authored
  in panel-core/docs/...'
last_updated: '2026-10-02'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/architecture/ECOSYSTEM_MANIFEST.md
managed_by: sync_private_docs
translation_status: pending
---
# NOVUS-OS Ecosystem Manifest

**Status:** normative cross-repository architecture contract  
**Scope:** `panel-core`, `agent-core`, and `installer`  
**Canonical source:** this document is authored in `panel-core/docs/architecture/` and synchronized verbatim to the root of each repository.

## 1. Product Vision & Architecture Philosophy

NOVUS-OS is a Web-OS for operating managed infrastructure through one browser-native control surface. It replaces fragmented external administration tools such as WinSCP and PuTTY with permissioned product workflows: file management, terminal access, service and container lifecycle, networking, backups, websites, databases, telemetry, and security administration.

The product has two complementary UI modes:

| Mode | Purpose |
| --- | --- |
| **Dashboard** | Fast operational overview: health, telemetry, alerts, queues, inventory, and high-frequency actions. |
| **WebDesktop** | A persistent, multi-tool workspace for authenticated operators, with routed panels for files, terminals, instances, websites, databases, and administration. |

The frontend is a browser application with a shell, hash routing, lazy-loaded Vue feature modules, shared runtime UI services, i18n, and PWA lifecycle support. PWA is a delivery and resilience property of the Panel UI; it never transfers host authority to the browser.

Architecture follows strict control/data/bootstrap separation:

1. The Panel decides *who may request what*, persists intent and state, and presents results.
2. The Agent performs privileged, host-local work only after an authenticated transport request.
3. The Installer prepares a host once, transfers durable ownership to Panel and Agent, then removes its own bootstrap surface.

## 2. Tripartite Boundary Matrix

| Repository / role | Allowed and owned | Strictly prohibited |
| --- | --- | --- |
| **`panel-core` - Brain / Control-Plane** | PHP application, Vue/PWA UI, PostgreSQL-backed product state, IAM/OIM policy evaluation, API routing, orchestration, audit trails, command intent, connection metadata, business rules, and presentation of Agent results. | Direct root-level host administration; direct Docker socket use; raw host filesystem mutation; local PTY ownership; embedding privileged Bash or `sudo` workflows as a replacement for Agent RPC. New code must use the Agent facade and typed transport contracts. |
| **`agent-core` - Hands and feet / Data-Plane** | Long-running Go daemon, authenticated gRPC services, host probes, Docker and system operations, VFS enforcement, container filesystem operations, PTY streaming, telemetry collection, and management of canonical instance volumes. | Web UI, browser session/authentication flows, product IAM/OIM policy decisions, PostgreSQL control-plane state, business workflow orchestration, or direct coupling to Panel internals and database schema. |
| **`installer` - Ephemeral bootstrapper** | Root-only preflight, dependency installation, download and verification of versioned release artifacts, initial deployment/configuration, initial secrets/bootstrap manifest, terminal installation progress, and post-install health check. | Becoming a permanent service, acting as the Panel runtime, retaining user credentials after completion, implementing ongoing host lifecycle operations, or remaining on a successful production host. |

The Installer owns a temporary setup protocol only: a token-gated embedded UI, `POST /api/setup`, and `GET /api/stream` for text status frames and binary PTY output. This is not a Panel-to-Agent control channel and does not grant the browser any durable host authority.

### Panel Domain Ownership

`panel-core/app/Modules` is the Panel's application boundary. Its domains are `SystemCore`, `SecurityIAM`, `RuntimeInstances`, `WebsitesVHosts`, `Databases`, `MonitoringTelemetry`, `FilesVFS`, `AgentTransportFederation`, and `PlatformOps`.

`routes/api.php` composes the public HTTP contract from those module route files. Controllers are HTTP/permission adapters; services own business behavior; `NovusAgentClient` and its direct/federated drivers are the canonical Panel-to-Agent integration surface.

### Compatibility Debt Is Not Authority

The Panel contains legacy local shell/Docker access paths, including `DashboardController` and a local container-log fallback. They are compatibility debt, not precedent. They must not be copied, extended, or used for new functionality. A replacement must preserve the external HTTP contract while relocating execution to the Agent transport boundary.

## 3. Inter-Process Communication Contract

Panel-to-Agent communication is gRPC-first. The authoritative protobuf definitions live in `agent-core/proto/`; the Panel uses raw protobuf codec and transport drivers only to implement those contracts. The current gRPC server registers `NovusAgent`, `NovusRuntimeSurface`, `InstanceService`, and `BackupService`.

| Aspect | Contract |
| --- | --- |
| Transport | TLS is mandatory for the Agent gRPC listener. Panel selects a direct or federated driver from node metadata; direct runtime operations are gRPC-first. HTTP fallback, where explicitly configured for compatibility, is not a contract for new features. |
| Authentication | Each privileged request carries `x-panel-uuid`, `x-request-timestamp`, and `x-signature`. The Agent validates an HMAC-SHA256 over the protobuf payload followed by the timestamp, a 15-second default clock window, the Panel lock, replay protection, rate limits, and security audit logging before executing work. Pairing and standard gRPC health are the deliberately unsigned exceptions. |
| Authorization | The Panel evaluates user IAM/OIM rights before issuing intent. The Agent enforces only its own narrow operation/scoping boundary and never treats browser input as authorization. |
| Identity and correlation | Requests use node identity and a request UUID. Logs, events, errors, and state acknowledgements preserve that correlation ID across the boundary. |
| Unary operations | Host information, container lifecycle, VFS, websites, SSL, system operations, backup operations, and telemetry queries use typed protobuf request/response messages. The Panel sends an Agent DSL, not raw Docker API payloads. |
| Server streams | Instance provisioning and container pull progress use typed server streams; logs, telemetry, and other continuous outputs must follow bounded, cancellable stream contracts and preserve correlation IDs. |
| Bidirectional PTY | Terminal input/output uses `NovusAgent.PtyStream` frames (`open`, `input`, `resize`, `output`, `exit`, `error`). The Agent permits only configured shell paths and starts commands without shell interpolation. The browser never opens an unauthenticated host PTY; the Panel authorizes and relays the user session through the Agent contract. |

Neither repository may change protobuf service names, message fields, metadata names, signing rules, or stream semantics independently. A contract change requires coordinated source, generated/codec support, Panel call-site, Agent handler, and focused compatibility tests in the same release plan.

## 4. Storage & Filesystem Topology Standard

The canonical physical storage root for managed persistent data is:

```text
/var/lib/novus/volumes/
├── games/      # Game-server instance volumes
├── service/    # Application and service instance volumes
└── web/        # Docker website and web-container volumes
```

`/www/containers` is a navigation entry point, not a second storage tree:

```text
/www/containers -> /var/lib/novus/volumes/web
```

The remaining host boundary is:

```text
/www/panel/                 # Deployed Panel application, never a tenant volume
/www/sites/                 # Classic host-level sites, independently isolated
/etc/novus/secrets/         # Secrets outside the web root
/etc/novus/secrets/panel-novus.env
/etc/novus/agent.yaml       # Encrypted Agent pairing state and master secret
/etc/novus/tls/             # Agent gRPC TLS key material
/etc/novus/manifest.json    # Durable bootstrap/host identity metadata
```

Secrets must remain outside `/www/panel` and outside tenant/container mounts. In particular, production Panel configuration is loaded from `/etc/novus/secrets/panel-novus.env` with the least permissions needed by the Panel service (`0640 www-data:www-data` in the installer baseline); a `.env` file under `/www/panel` is a security violation. Agent state, TLS private keys, master keys, JWT material, and installer audit records are host secrets and must not be mounted into tenant containers. The Agent must resolve volume paths through its constrained VFS/instance rules and must not allow traversal between tenant roots, Panel files, or secret paths.

### Current Implementation Variances

The following are audited facts, not approvals for new code:

| Surface | Current fact | Required direction |
| --- | --- | --- |
| Panel host execution | Legacy `DashboardController` and local log compatibility paths still invoke Docker/shell locally. | Preserve the external API while moving execution to `NovusAgentClient` and typed Agent RPC. |
| Agent VFS policy | `internal/grpcserver/server.go` currently constructs VFS with `AllowedRoots: []string{"/"}`. It preserves host-administrator access, but does not enforce the scoped-volume standard for ordinary runtime work. | Split policy explicitly into `host_admin` and scoped instance/site/game modes; default runtime scopes to `/var/lib/novus/volumes/*` and test symlink traversal. |
| Agent contract source | The live server registers `BackupService`, while the checked-in source `.proto` files do not declare it; `NovusFileSystem` is declared but is not registered by the current server composition root. | Reconcile source `.proto`, generated stubs, server registration, Panel codec/call sites, and compatibility tests before changing either surface. |
| Agent auxiliary transports | The current daemon also starts HTTP WebSocket-console and SSH/SFTP listeners for compatibility. | Treat them as Agent transport adapters, not a second product UI or policy layer; converge their authentication and scope checks with the gRPC boundary. |
| Installer artifact integrity | The installer currently verifies basic download success/minimum size and archive readability, but does not yet enforce release checksums for every Panel and Agent artifact. | Obtain versioned release metadata and require SHA-256 verification before activating an artifact. |
| Installer preflight | The runtime preflight currently gates only ports `80` and `443`; the installer master-plan requires parity checks for `8080` and `9443` too. | Validate all externally bound bootstrap and Agent ports before production installation, while retaining explicit `--dev` downgrade behavior. |
| Installer session transport | The temporary setup server currently binds `:8080`, issues a 128-bit URL token, and sets an `HttpOnly`/`SameSite=Strict` cookie without the `Secure` attribute. | Keep the short-lived token gate, restrict exposure to the installation session, and complete the planned cookie/transport hardening before treating the endpoint as production-safe. |

## 5. Autonomous AI Directives

Before any task, an AI agent must read the repository-local `ECOSYSTEM_MANIFEST.md` and preserve these boundaries.

### When Working in `panel-core`

- Implement product policy, persistence, IAM/OIM, API contracts, services, UI, and orchestration only.
- Do not add `shell_exec`, `exec`, `system`, `sudo`, Docker socket access, root commands, direct host VFS mutation, or long-lived PTY ownership.
- Express host intent through `NovusAgentClient` and the protobuf-backed driver boundary; preserve the Panel's HTTP/OpenAPI contracts when migrating legacy code.
- Treat agent response data as untrusted transport input until validated and mapped to Panel domain objects.

### When Working in `agent-core`

- Implement typed gRPC handlers, signed-request validation, replay defense, host-local execution, VFS containment, telemetry, and PTY stream handling.
- Do not add a Web UI, browser authentication/session implementation, Panel database access, or business/IAM policy engine.
- Do not widen privileges or filesystem roots merely to satisfy a Panel convenience request; evolve the typed contract and validation together.

### When Working in `installer`

- Implement only repeatable preflight/bootstrap steps, release acquisition and validation, initial configuration, installation telemetry, and final health verification.
- Keep every side effect idempotent and make `--dry-run` side-effect-free.
- Download compiled/versioned release artifacts from the approved GitHub distribution sources; do not compile or become the production control plane.
- In non-development, non-dry-run success paths, resolve the current executable with `os.Executable()` and remove it after emitting the final completion event. Do not self-delete on failure, development, or dry-run paths.

### Cross-Repository Rules

- Do not duplicate another repository's authority to avoid an RPC or deployment change.
- Do not expose secrets, private keys, raw credentials, or host-level paths in browser payloads, logs, telemetry, or repository files.
- Keep migrations and install/configuration steps idempotent.
- Changes crossing a boundary must update the relevant contract, documentation, focused tests, and release sequencing together.
