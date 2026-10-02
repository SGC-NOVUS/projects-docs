---
id: agent-core-configuration
cluster: novus-os
category: agent-core-general
order: 100
status: active
version: 0.1.0
title: 'NOVUS Agent-Core: Configuration Reference'
description: The authoritative configuration source is internal/config/config.go.
  All supported Agent settings are environment variables; undocumented variables are
  not a supported interface.
last_updated: '2026-10-02'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/agent-core
source_branch: main
source_path: docs/CONFIGURATION.md
managed_by: sync_private_docs
translation_status: pending
---
# NOVUS Agent-Core: Configuration Reference

The authoritative configuration source is `internal/config/config.go`. All supported Agent settings are environment variables; undocumented variables are not a supported interface.

## Listener And TLS

| Variable | Default | Purpose |
| --- | --- | --- |
| `NOVUS_AGENT_HTTP_LISTEN` | `:8080` | Compatibility HTTP/WebSocket listener address. |
| `NOVUS_AGENT_GRPC_LISTEN` | `:9443` | TLS-protected gRPC listener address. |
| `NOVUS_AGENT_WS_ALLOWED_ORIGINS` | derived from `NOVUS_AGENT_PANEL_URL` origin plus `http://127.0.0.1,http://localhost` fallback | Comma-separated WebSocket origin allowlist; requests with non-allowlisted `Origin` are rejected. |
| `NOVUS_AGENT_SSH_LISTEN` | `:2022` | Compatibility SSH/SFTP listener address. |
| `NOVUS_AGENT_SSH_HOST_KEY_FILE` | `<dirname(NOVUS_AGENT_STATE_FILE)>/ssh_host_rsa_key` | Persistent SSH host private key path (created if missing, reused across restarts). |
| `NOVUS_AGENT_TLS_CERT` | Agent-managed TLS certificate location | TLS certificate for the gRPC listener. |
| `NOVUS_AGENT_TLS_KEY` | Agent-managed TLS key location | Private key paired with the TLS certificate. Do not place key material in repository files or public examples. |
| `NOVUS_AGENT_TLS_AUTOGEN_DIR` | Agent-managed TLS directory | Location used when the Agent creates or rotates a self-signed certificate. |

TLS is mandatory for gRPC. If certificate material is absent, the Agent can bootstrap a self-signed certificate; operators should use the approved deployment procedure to establish trust.

For SSH/SFTP compatibility transport, the Agent persists the host key to the configured path and enforces private-key file permissions during load.

For WebSocket console compatibility transport, include session context query params (`session_uuid` or `session_id`) and node context (`node_uuid` or `node_id`) so JWT context-binding checks can be enforced.
The adapter accepts both query-key aliases and validates JWT context claims against the resolved node/container/session binding.
The Agent can also sync the in-memory WebSocket allowlist at runtime from authenticated gRPC metadata without restart:
- `x-novus-ws-allowed-origins`: comma-separated origin list.
- `x-novus-panel-url`: panel URL used to derive origin plus safe local fallback origins.

## State And Security

| Variable | Default | Purpose |
| --- | --- | --- |
| `NOVUS_AGENT_STATE_FILE` | Agent state-file location | Encrypted local pairing state. Compatibility alias: `NOVUS_AGENT_STATE_PATH` (startup deprecation warning emitted when alias is active). |
| `NOVUS_AGENT_STATE_ENCRYPTION_KEY` | empty | Optional state-encryption key supplied by the secure host environment. |
| `NOVUS_AGENT_PAIRING_TOKEN_TTL_MINUTES` | `15` | Lifetime of a pairing token; values below one minute fall back to `15`. |
| `NOVUS_AGENT_ALLOWED_CLOCK_SKEW_SECONDS` | `15` | Accepted request-clock skew for signed gRPC requests. |
| `NOVUS_AGENT_RATE_LIMIT_PER_MINUTE` | `600` | Per-panel request rate limit. |
| `NOVUS_AGENT_RATE_LIMIT_BURST` | `120` | Token-bucket burst capacity. |
| `NOVUS_AGENT_AUDIT_LOG_ENABLED` | `true` | Enables structured Agent security audit events. |

## Runtime, Files And Telemetry

| Variable | Default | Purpose |
| --- | --- | --- |
| `NOVUS_AGENT_DOCKER_SOCKET` | system Docker socket | Docker transport used by Agent runtime operations. |
| `NOVUS_AGENT_VFS_POLICY_MODE` | `host_admin` | VFS policy mode: `host_admin` allows host-wide VFS roots, `scoped_runtime` restricts to configured runtime roots. |
| `NOVUS_AGENT_VFS_SCOPED_ROOTS` | `/var/lib/novus/volumes/games,/var/lib/novus/volumes/service,/var/lib/novus/volumes/web` | Comma-separated scoped roots used when `NOVUS_AGENT_VFS_POLICY_MODE=scoped_runtime`. Compatibility alias: `NOVUS_AGENT_VFS_ALLOWED_ROOTS` (startup deprecation warning emitted when alias is active). |
| `NOVUS_AGENT_VFS_UPLOAD_DIR` | Agent-managed upload directory | Temporary storage for resumable file uploads. |
| `NOVUS_AGENT_VFS_WORK_DIR` | Agent-managed work directory | Temporary storage for file and archive operations. |
| `NOVUS_AGENT_SSL_CERT_DIR` | Agent-managed certificate directory | Read-only source for website certificate metadata. |
| `NOVUS_AGENT_BACKUP_DIR` | Agent-managed backup directory | Local backup working directory. |
| `NOVUS_AGENT_TELEMETRY_DISK_MOUNT` | `/` | Disk mount used for host telemetry. |

The runtime resolves VFS roots via policy mode:
- `host_admin`: host-wide root scope for explicit administrator workflows.
- `scoped_runtime`: baseline isolation to configured runtime volume roots.

Set the mode explicitly in production to match your operational intent.

Legacy compatibility note: if only `NOVUS_AGENT_VFS_ALLOWED_ROOTS` is set (without explicit `NOVUS_AGENT_VFS_POLICY_MODE`), the loader maps behavior to `scoped_runtime` for backward compatibility.

## Canonical Key Migration

Use canonical keys in all new deployments and automation. Legacy aliases are compatibility-only and emit startup warnings when used as the active source.

| Deprecated alias | Canonical key | Runtime behavior |
| --- | --- | --- |
| `NOVUS_AGENT_STATE_PATH` | `NOVUS_AGENT_STATE_FILE` | Alias is read only when canonical key is unset; startup warning event `config_deprecated_env_alias_used` is emitted. |
| `NOVUS_AGENT_VFS_ALLOWED_ROOTS` | `NOVUS_AGENT_VFS_SCOPED_ROOTS` | Alias is read only when canonical key is unset; startup warning event `config_deprecated_env_alias_used` is emitted. |

Precedence rule: canonical key wins when both canonical and legacy alias are set.

## PTY

| Variable | Default | Purpose |
| --- | --- | --- |
| `NOVUS_AGENT_PTY_SHELL` | `/bin/bash` | Default interactive shell. |
| `NOVUS_AGENT_PTY_CWD` | `/` | Default PTY working directory. |
| `NOVUS_AGENT_PTY_ALLOWED_SHELLS` | Approved shell allowlist | Comma-separated shell paths allowed for PTY sessions. |

The Agent validates the selected shell against the configured allowlist. Browser clients do not connect to the host PTY directly; terminal sessions remain behind the Panel-to-Agent transport contract.

## Panel Compatibility

| Variable | Default | Purpose |
| --- | --- | --- |
| `NOVUS_AGENT_PANEL_URL` | empty | Optional Panel URL for compatibility workflows. |
| `NOVUS_AGENT_PANEL_TOKEN` | empty | Optional Panel token for compatibility workflows. Supply it only through the approved secret-management path. |

## Safe Configuration Example

```ini
NOVUS_AGENT_GRPC_LISTEN=:9443
NOVUS_AGENT_ALLOWED_CLOCK_SKEW_SECONDS=15
NOVUS_AGENT_RATE_LIMIT_PER_MINUTE=600
NOVUS_AGENT_RATE_LIMIT_BURST=120
NOVUS_AGENT_AUDIT_LOG_ENABLED=true
NOVUS_AGENT_PTY_SHELL=/bin/bash
NOVUS_AGENT_PTY_ALLOWED_SHELLS=/bin/bash,/bin/sh
```

Do not copy secret values, TLS private-key locations, pairing tokens, or Panel tokens into documentation, source control, shell history, or process arguments.
