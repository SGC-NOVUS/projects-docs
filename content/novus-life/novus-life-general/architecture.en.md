---
id: novus-life-architecture
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: 'Architecture Overview: Novus Life'
description: '**Novus Life** is a private, offline-first utility and home expense
  management platform designed and maintained by **SGC-NOVUS** (System Generation
  Core). It combines client-sid...'
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/ARCHITECTURE.md
managed_by: sync_private_docs
---
# Architecture Overview: Novus Life

**Novus Life** is a private, offline-first utility and home expense management platform designed and maintained by **SGC-NOVUS** (System Generation Core). It combines client-side cryptographic isolation with an autonomous server infrastructure.

---

## 1. High-Level Architecture

The system operates on a **Hybrid Storage & Offline-First Model**:
1. **Primary Client Layer (IndexedDB via Dexie.js)**:
   - All immediate interactions, meter reading inputs, tariff evaluations, and history views execute directly against local IndexedDB.
   - Guarded against OS-level cache eviction using the **Persistent Storage API** (`navigator.storage.persist()`).
   - Ensures 100% operational capability in offline environments (e.g., basements, utility shafts, disconnected networks).
2. **Server Synchronization Layer (Self-Hosted VPS)**:
   - Built with **Node.js 22+ (Express + pg driver)** and **PostgreSQL 16**.
   - Accessible via strictly internal proxying behind Nginx under domain `https://novus-life.online/api/*`.
   - Data is committed in atomic SQL transactions (`BEGIN ... COMMIT`) to prevent partial sync states.
   - All relational entities use **UUIDv7** (RFC 9562) primary keys for timestamp-ordered indexing without B-Tree page fragmentation.
3. **Backup Layer (Google Drive `appDataFolder`)**:
   - Optional encrypted archive synchronization using Google Drive's hidden `appDataFolder` (`https://www.googleapis.com/auth/drive.appdata`).
   - Isolated from user root files, preventing accidental manual deletion.

```
+-------------------------------------------------------------------------+
|                              CLIENT DEVICE                              |
|                                                                         |
|  +--------------------+     +----------------------------------------+  |
|  |   Vue 3 UI Layer   | <-> |       Web Crypto API (AES-256-GCM)     |  |
|  +--------------------+     +----------------------------------------+  |
|            |                                     |                      |
|  +--------------------+             +--------------------------+        |
|  | Dexie.js (IndexedDB|             | Encrypted Cipher Payload |        |
|  | Persistent Storage |             +--------------------------+        |
|  +--------------------+                          |                      |
+------------|-------------------------------------|----------------------+
             | (HTTPS POST/GET /api/sync)          | (HTTPS OAuth2/appData)
             v                                     v
+-----------------------------+       +-----------------------------------+
|     NOVUS LIFE VPS API      |       |       GOOGLE DRIVE APPDATA        |
|  Node.js 26 + PostgreSQL 18 |       |  Hidden Isolated Container        |
|  UUIDv7 Keys + Bcrypt / JWT |       |  novus_life_vault.json.enc        |
+-----------------------------+       +-----------------------------------+
```

---

## 2. PWA and WebAPK Lifecycle

### Android (WebAPK)
- On modern Android devices (Chrome, Edge, Samsung Internet), Novus Life meets all WebAPK criteria (valid manifest, standalone display mode, maskable and standard icons, registered service worker).
- The operating system mints a genuine Android package (`org.chromium.webapk.*`) granting:
  - An isolated Linux UID sandbox distinct from browser tab processes.
  - An independent application entry in **Android Settings -> Apps -> Novus Life**.
  - System-level permission toggles (Camera for meter photo capture, Push Notifications for payment reminders).
  - Storage allocation reporting (IndexedDB cache reported accurately to OS settings).

### Desktop (Windows, macOS, Linux)
- Runs in standalone window mode with `window-controls-overlay` and system theme synchronization.

### Apple iOS
- Runs via Safari Web App ("Add to Home Screen") in full-screen standalone mode with touch optimization.

---

## 3. Data Flow & Cryptographic Boundaries

1. **Local Record Creation**:
   - The user inputs utility readings (e.g., electricity T1/T2, cold water, gas).
   - Reading differences and sums are calculated on-the-fly using the active tariff schedule.
   - The record is persisted into IndexedDB with a unique local UUIDv7.
2. **Cryptographic Protection (Zero-Knowledge)**:
   - Sensitive payloads are passed to `cryptoVault.encrypt()` (Web Crypto API AES-256-GCM).
   - The derived master key is held exclusively in client runtime memory (PBKDF2 with 100,000 iterations).
   - Only encrypted ciphertext is sent to remote endpoints.
3. **Synchronization**:
   - The synchronization service transmits batch records via `/api/sync` authenticated by a standard JSON Web Token (JWT).
   - The PostgreSQL database persists entity rows with cascade deletion (`ON DELETE CASCADE`) tied to `user_id`.

---

## 4. Technology Matrix

| Layer | Technology | Role |
|---|---|---|
| **Runtime** | Node.js 26.x Active | Backend API runtime |
| **Database** | PostgreSQL 18 (Docker) | Relational database engine |
| **API Framework** | Express 5.0.x+ / TypeScript | HTTP API routing and validation |
| **Primary Keys** | UUIDv7 (RFC 9562) | Millisecond-ordered, collision-free identifiers |
| **Frontend Framework** | Vue 3.5+ Composition API | Reactive web interface |
| **State Management** | Pinia 3.x | Client state and session store |
| **Styling Engine** | Tailwind CSS v4 | Utility-first CSS system |
| **Local Database** | Dexie.js 4.x (IndexedDB) | Offline-first client datastore |
| **Cryptographic Engine** | Web Crypto API | Client-side AES-256-GCM |
| **Reverse Proxy** | Nginx 1.24+ | SSL termination, reverse proxying, static caching |
| **Ecosystem** | SGC-NOVUS | Architectural ownership and release lifecycle |
