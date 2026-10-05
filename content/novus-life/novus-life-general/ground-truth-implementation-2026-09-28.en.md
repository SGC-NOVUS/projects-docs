---
id: novus-life-ground-truth-implementation-2026-09-28
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: 'Ground truth: Novus Life implementation'
description: '**Status:** internal static audit of the checkout on 2026-09-28. **Scope:**
  Vue/PWA routes, Express backend, PostgreSQL, Google integrations, email, browser
  storage and environm...'
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/GROUND_TRUTH_IMPLEMENTATION_2026-09-28.md
managed_by: sync_private_docs
---
# Ground truth: Novus Life implementation

**Status:** internal static audit of the checkout on 2026-09-28.
**Scope:** Vue/PWA routes, Express backend, PostgreSQL, Google integrations, email, browser storage and environment configuration.

## Current architecture

The repository is not the React template described by its root README. The tracked implementation is:

| Layer | Actual implementation |
| --- | --- |
| Browser | Vue 3, Vite, Vue Router, Pinia, i18n and PWA assets |
| Local client data | Browser storage/device capability services and domain stores for addresses, services, tariffs, meter readings, payments and reminders |
| API | Express on `0.0.0.0`, `PORT` default `3001`; CORS origin is `*`; JSON/urlencoded bodies limited to 15 MiB |
| Persistence | PostgreSQL through `pg` Pool; server refuses to listen after 10 unsuccessful connection attempts separated by 2 seconds |
| Identity | Email/password JWT plus Google OAuth; bearer JWT lifetime is 60 days |
| Cloud backup | Google Drive `appDataFolder`, receiving an opaque encrypted payload from the client |
| Mail | Resend; no API key switches mail to a logging mock that returns success |

## Browser navigation and modules

| Route area | Implemented modules |
| --- | --- |
| Public | Landing, privacy, terms, about, auth |
| `/app` | Dashboard, profile, utilities, tariffs, addresses, services, payments, reminders, analytics, settings |
| Compatibility | Legacy short URLs redirect to `/app/*`; unknown paths redirect to `/` |
| PWA behavior | Landing redirects to `/app` when launched from standalone/PWA context |

The frontend API client uses same-origin relative calls, adds a bearer token from `localStorage`, and throws on non-2xx responses (`src/core/services/api-client.ts`).

## API catalogue

| Prefix | Operations | Auth | Purpose |
| --- | --- | --- | --- |
| `/api/health` | `GET` | No | API process health payload |
| `/api/auth` | `POST /register`, `POST /login`, `GET /me`, `PUT /profile`, `POST /password/set`, `POST /password/change`, `POST /verify-email/request`, `GET /verify-email/confirm`, `GET /google/url`, `GET /google/callback`, `POST /google/exchange` | Mixed; profile/password/verify request require bearer token | Identity, profile, email verification and Google OAuth |
| `/api/sync` | `GET /`, `POST /` | Bearer token | Restore and transactionally upsert user addresses, services, tariffs, utilities, regular payments and reminders |
| `/api/drive` | `GET /status`, `POST /backup`, `GET /restore` | Bearer token | Store/retrieve client-encrypted backup in Google Drive appDataFolder |

The server mounts these groups in `server/src/index.ts`. There is no OpenAPI specification in the repository.

## Persistence and failure behavior

`checkDbConnection()` retries `SELECT NOW()` ten times and runs additive `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` migrations after successful connection. A failed database check exits the process before `listen()`.

`POST /api/sync` wraps all table upserts in a PostgreSQL transaction. On an error it executes `ROLLBACK`, returns a `500`, and always releases the pool client. The API treats client-side local IDs as inputs, maps them to UUIDv7 values, and defaults missing domain fields while importing.

Google Drive backup stores the supplied `encryptedPayload` as `novus_life_vault.json.enc` in the user's hidden `appDataFolder`; the server does not decrypt the payload. Missing refresh token returns a normal "not connected"/`400` response depending on endpoint. OAuth failures surface as `500` in exchange and redirects with error query parameters in callback flow.

Browser persistent-storage requests are best effort. A denied `navigator.storage.persist()` request is returned as a user-facing non-persisted result; it does not block the application (`src/core/services/storage-manager.ts`).

## Environment registry

| Variable | Type/default | Where used | Criticality |
| --- | --- | --- | --- |
| `PORT` | integer; `3001` | `server/src/index.ts` | Startup boundary |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `db`, `5432`, `novus_life`, `novus_user`, `novus_secret_pass_2026` | `server/src/db.ts` | **Critical** for production persistence; fallback password is unsafe |
| `JWT_SECRET` | secret; `novus_life_default_jwt_secret_dev` | `server/src/auth.ts` | **Critical** for production identity; insecure fallback is active if omitted |
| `APP_URL` | URL; `https://novus-life.online` | Auth redirects and email links | Feature-critical for OAuth/email links |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | strings; empty | Google OAuth and Drive refresh flows | Feature-critical only for Google features |
| `RESEND_API_KEY` | secret; empty | Resend initialization | Feature-critical for actual email delivery; absent key enables logging mock |
| `EMAIL_FROM_AUTH`, `EMAIL_FROM_NOTIFY`, `EMAIL_REPLY_TO` | sender strings with product defaults | `server/src/services/email.ts` | Feature-critical only for email branding/delivery |
| `VITE_APP_NAME`, `VITE_APP_URL` | frontend template values | `.env.example` | No current `import.meta.env` consumer was found in `src` |
| `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` | frontend template values | `.env.example` | No current `import.meta.env` consumer was found in `src`; they are not evidence of active Supabase runtime use |

`server/.env.example` exists and documents server database, JWT, Google and email values. The root `.env.example` documents only Vite/Supabase/Google/email and omits backend `PORT`, `DB_*`, `JWT_SECRET` and `APP_URL`; operator documentation must point to the server template for backend deployment.

## Confirmed documentation gaps

1. Replace the root React-template README with Vue + Express + PostgreSQL documentation.
2. Add an API reference generated from the three mounted Express routers.
3. Remove insecure production defaults for JWT and database password, or make startup reject them outside development.
4. Clarify that current client sync targets the self-hosted Express API; Supabase values in the root template are not currently consumed by browser code.
