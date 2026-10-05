---
id: novus-life-privacy-policy
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: Privacy Policy
description: '**Effective Date**: September 8, 2026 **Application**: Novus Life (https://novus-life.online)
  **Ecosystem**: SGC-NOVUS (System Generation Core) **Compliance**: Google API Servic...'
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/PRIVACY_POLICY.md
managed_by: sync_private_docs
---
# Privacy Policy

**Effective Date**: September 8, 2026  
**Application**: Novus Life (`https://novus-life.online`)  
**Ecosystem**: SGC-NOVUS (System Generation Core)  
**Compliance**: Google API Services User Data Policy, General Data Protection Regulation (GDPR)

---

## 1. Zero-Knowledge Architecture & Data Sovereignty

Novus Life is built on the fundamental principle that utility and personal financial records belong exclusively to the individual user. We implement a **Zero-Knowledge** security model:
- All sensitive entries—including meter readings, billing amounts, property addresses, and notes—are encrypted client-side using **AES-256-GCM** via the browser's hardware-accelerated **Web Crypto API**.
- The server stores only opaque cryptographic ciphertext. Server administrators and unauthorized third parties cannot decrypt or read user data.
- Decryption occurs strictly inside the device's volatile memory using a key derived on the client (PBKDF2 with 100,000 rounds).

---

## 2. Google API Services User Data Policy Compliance

Novus Life strictly adheres to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

### 2.1 Identity Scopes (`openid`, `userinfo.email`, `userinfo.profile`)
- **Purpose**: Authenticating the user account and establishing a secure session on `novus-life.online`.
- **Data Collected**: Email address, display name, and avatar picture URL.
- **Usage Restrictions**: We never sell, rent, or transfer email addresses to third parties, data brokers, or advertising networks.

### 2.2 Application Data Scope (`https://www.googleapis.com/auth/drive.appdata`)
- **Purpose**: Optional encrypted database backup and cross-device restoration.
- **Strict Isolation**: Access is strictly limited to the application-specific hidden directory (`appDataFolder`).
- **Safety Guarantee**: Novus Life **cannot access, read, view, modify, or delete** any personal files, documents, spreadsheets, photos, or folders outside of its dedicated `novus_life_vault.json.enc` backup file.

---

## 3. Local Storage and System Permissions

### 3.1 Persistent Storage (`navigator.storage.persist()`)
The application requests persistent storage status to protect the client-side IndexedDB database against automatic cache purge routines triggered by operating system disk constraints.

### 3.2 Camera Access
Camera permissions are requested solely on-demand to capture physical utility meter dials for optical reference. Captured images are compressed locally and never uploaded to public cloud vision APIs.

### 3.3 System Notifications
Notifications are used exclusively on-device to inform the user of approaching billing deadlines and meter submission schedules.

---

## 4. User Rights and Data Deletion (Right to Be Forgotten)

Users retain complete ownership over their data at all times:
- **Local Data**: Can be purged immediately via the application settings.
- **Server Account Deletion**: Users may request or initiate permanent account deletion. This immediately triggers a database cascade (`ON DELETE CASCADE`), removing all user records, authentication credentials, and synchronization states without archival backups.
- **Inquiries**: For data protection inquiries or formal deletion requests, contact: `support@novus-life.online`.
