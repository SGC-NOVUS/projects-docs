---
id: novus-edo-ground-truth-implementation-2026-09-28
cluster: novus-edo
category: novus-edo-general
order: 100
status: active
version: 0.1.0
title: 'Ground truth: Novus Flow.EDO implementation'
description: '**Status:** internal static audit of the checkout on 2026-09-28. **Scope:**
  Vue frontend routes, Express server composition, Prisma/R2 persistence, crypto,
  converter and environ...'
last_updated: '2026-10-02'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-edo
source_branch: main
source_path: docs/GROUND_TRUTH_IMPLEMENTATION_2026-09-28.md
managed_by: sync_private_docs
---
# Ground truth: Novus Flow.EDO implementation

**Status:** internal static audit of the checkout on 2026-09-28.
**Scope:** Vue frontend routes, Express server composition, Prisma/R2 persistence, crypto, converter and environment reads. This document describes implemented behavior, not a compliance or legal certification.

## Executable shape

The application is a Vue/Vite browser client plus an Express API started through `tsx server/index.ts`.

| Surface | Actual implementation |
| --- | --- |
| Browser UI | Vue 3, Vue Router, Pinia and client-side signing services |
| API | Express 5 on `PORT`, default `3001` |
| Persistence | Prisma 7 with MariaDB adapter; `DATABASE_URL` fallback is `mysql://novus:novus123@localhost:3306/novus_edo` |
| Object storage | Cloudflare R2 through AWS S3 SDK, with presigned upload/download URLs |
| Mail | Resend plus Vue Email rendering |
| Converter | Independent HTTP service on `127.0.0.1:4174`, spawning LibreOffice (`SOFFICE_PATH` or `soffice`) |
| Browser signing | Document private keys remain browser-side according to the implemented client architecture; server persists signature artifacts and metadata |

`server/index.ts` loads dotenv, rejects missing/sentinel `JWT_SECRET` only when `NODE_ENV=production`, installs CORS with `CORS_ORIGIN` or `*`, mounts routes, and serves `dist/` in production.

## Browser routes

| Route | Auth requirement | Implemented view/meaning |
| --- | --- | --- |
| `/`, `/about`, `/privacy`, `/terms`, `/login`, `/register` | No | Public, legal and identity screens |
| `/dashboard` | Yes | Currently reuses `Inbox.vue` |
| `/documents`, `/documents/new`, `/documents/:id` | Yes | Document list, creation and detail workflow |
| `/contacts`, `/archive`, `/settings` | Yes | Address book, archive and settings |
| `/features`, `/pricing` | No | Redirect to `/` |

The navigation guard fetches the current user when a token exists and redirects unauthenticated protected navigation to `/login` (`src/router/index.ts`).

## Express API catalogue

All paths below have the `/api` prefix shown in the first column.

| Prefix | Operations | Authentication | Purpose |
| --- | --- | --- | --- |
| `/health` | `GET` | No | Basic process health response |
| `/proxy` | `POST` | No | Binary proxy for EUSign CMP/TSP/OCSP traffic |
| `/auth` | `POST /register`, `POST /login`, `GET /verify-email`, `GET /me` | `/me` requires bearer token | Email/password and KEP/TIN login, registration and verification |
| `/users` | `PUT /me`, `PUT /me/password` | Bearer token | Update profile/email and set/change password |
| `/organizations` | `GET /`, `POST /`, `GET /:id/members`, `POST /:id/members` | Bearer token | Organization membership and member management |
| `/documents` | `POST /`, `GET /`, `GET /tasks`, `POST /:id/sign`, `GET /:id/archive`, `GET /:id/download` | Bearer token | Legacy local-upload document workflow |
| `/v2/documents` | `GET /`, `GET /:id`, `POST /presigned-url`, `POST /`, `POST /:id/sign`, `DELETE /:id`, `POST /:id/cancel`, `GET /:id/archive` | Bearer token | DocumentPackage workflow with R2 storage and routing participants |
| `/public` | `POST /store-verification`, `GET /verify/:id`, `GET /verify/:id/protocol` | Store endpoint optionally accepts bearer token; reads are public | Public signature verification and protocol download |
| `/settings/document-types` | `GET`, `POST`, `POST /:id/toggle` | Bearer token | Global/workspace document type registry |

The API has no checked-in OpenAPI document. The router and these source files are the current HTTP contract.

## Data and object-storage behavior

There are two independent document persistence paths:

1. Legacy `/api/documents` uses Multer `uploads/` and stores local paths in the database. Original download reads that filesystem path; archive creation streams from this local state.
2. `/api/v2/documents` stores package metadata in Prisma and uses R2 object keys. It issues a five-minute presigned upload URL and uploads signatures/PAdES files to R2 after Multer receives them locally.

Public verification stores anonymous objects under `unclaimed/<RNOKPP>/<document UUID>/...`; authenticated submission uses `individuals/<user ID>/documents/<verification ID>/...`. It creates or reuses a fixed system account for anonymous persisted packages. R2 writes request `AES256` server-side encryption.

## Environment registry

| Variable | Type/default | Where used | Startup/feature criticality |
| --- | --- | --- | --- |
| `NODE_ENV` | string; production activates JWT enforcement and static serving | `server/index.ts` | Startup boundary |
| `PORT` | integer/string; `3001` | `server/index.ts` | Startup boundary |
| `DATABASE_URL` | MariaDB URL; insecure local fallback shown above | `server/db.ts` | Feature-critical for all persistence |
| `JWT_SECRET` | secret; production must differ from the sentinel | `server/index.ts`, `server/middleware/auth.ts` | Security-critical |
| `ENCRYPTION_KEY` | 64-hex-char secret; random process fallback | `server/utils/crypto.ts` | Security and data-read critical |
| `BLIND_INDEX_SECRET` | secret; random process fallback | `server/utils/crypto.ts` | Search/index continuity critical |
| `CORS_ORIGIN` | origin string; `*` | `server/index.ts` | Security boundary |
| `R2_ACCOUNT_ID`, `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_PRESIGNED_EXPIRES_IN` | R2 endpoint/credentials; expiration `900` seconds | `server/storageService.ts` | Feature-critical for v2/public objects |
| `RESEND_API_KEY`, `APP_URL` | mail secret and URL; `APP_URL` defaults to `http://localhost:5173` in EDO mail service | `server/emailService.ts` | Feature-critical for email delivery/links |
| `SOFFICE_PATH` | executable name/path; `soffice` | `server/converter.mjs` | Feature-critical only for conversion service |
| `REDIS_HOST`, `REDIS_PORT` | service-local environment reads | worker/queue code paths | Feature-critical only where queue worker is started |

No checked-in `.env.example` or `.env.sample` was found. The README mentions only part of this list and omits `ENCRYPTION_KEY`, `BLIND_INDEX_SECRET`, `NODE_ENV`, `PORT`, `R2_ACCOUNT_ID`, `R2_PRESIGNED_EXPIRES_IN`, `SOFFICE_PATH` and Redis settings.

## Failure modes and implementation limits

| Situation | Observed behavior |
| --- | --- |
| Missing/changed `ENCRYPTION_KEY` or `BLIND_INDEX_SECRET` | The process generates a new random key/secret. Previously encrypted fields cannot be decrypted and blind-index lookup continuity changes after restart. This must be treated as a production configuration failure, not a safe fallback. |
| Invalid encryption key length | Encrypt/decrypt throws because the parsed hex key is not 32 bytes. |
| Production JWT unset/sentinel | API logs critical error and exits before listening. |
| R2 unavailable | v2/public persistence calls fail and return server errors; temporary Multer files are not guaranteed to be cleaned on every exception path. |
| Email unavailable | Mail functions catch/log failures; primary auth/document flow may still return success. |
| Converter missing LibreOffice | `/api/convert` returns `422`; temporary directory cleanup runs in `finally`. |
| Converter input | Converter accepts one supported office file up to 25 MiB, runs LibreOffice without a shell, and listens only on loopback. |
| Public CMP proxy | The proxy accepts caller-provided target address, normalizes HTTP/HTTPS heuristically and makes an outbound POST without an implemented timeout or strict destination allow-list. It needs a dedicated security review before public exposure. |

## Documentation corrections required

1. Add a real environment template that includes all implemented secrets and state-continuity keys, with placeholders only.
2. Publish a generated OpenAPI contract from the Express route files before claiming a stable public API.
3. Document v1 local `uploads/` and v2 R2 persistence as separate, currently coexisting workflows.
4. Do not describe random crypto-key fallback as production-safe.
