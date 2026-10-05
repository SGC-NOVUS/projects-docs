---
id: novus-life-security
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: Security Architecture & Cryptographic Model
description: '**Project**: Novus Life **Maintainer**: SGC-NOVUS (System Generation
  Core) **Security Level**: Zero-Knowledge Client-Side Encryption (E2EE)'
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/SECURITY.md
managed_by: sync_private_docs
---
# Security Architecture & Cryptographic Model

**Project**: Novus Life  
**Maintainer**: SGC-NOVUS (System Generation Core)  
**Security Level**: Zero-Knowledge Client-Side Encryption (E2EE)

---

## 1. Threat Model & Design Principles

Novus Life is engineered under the assumption that central servers and communication channels can be subjected to inspection or unauthorized compromise. To guarantee user privacy under any conditions, the application implements a strict **Zero-Knowledge Architecture**:

1. **Client-Side Encryption Only**: Plaintext meter readings, property titles, financial amounts, and personal comments never reach server memory or disk storage.
2. **No Server Master Keys**: The central PostgreSQL database and API servers hold zero private keys or secret material capable of reversing client ciphertexts.
3. **Hardware-Accelerated Cryptography**: All cryptographic primitives rely on the standard W3C **Web Crypto API** (`crypto.subtle`).

---

## 2. Cryptographic Primitives & Specifications

### 2.1 Symmetric Encryption (AES-GCM-256)
- **Algorithm**: `AES-GCM` (Advanced Encryption Standard in Galois/Counter Mode).
- **Key Length**: 256 bits.
- **Initialization Vector (IV)**: 96-bit cryptographically secure pseudorandom value generated per operation via `crypto.getRandomValues()`.
- **Integrity Tag**: 128-bit authentication tag embedded directly into the GCM stream to detect tampering.

### 2.2 Key Derivation (PBKDF2)
- **Algorithm**: `PBKDF2` (Password-Based Key Derivation Function 2).
- **PRF**: `HMAC-SHA-256`.
- **Work Factor**: 100,000 iterations.
- **Salt**: Isolated project-specific entropy salt (`novus_life_zero_knowledge_salt_2026`).

---

## 3. Storage Security & OS Eviction Defense

### 3.1 Persistent Storage API
By default, web browsers treat IndexedDB as temporary storage subject to silent eviction under operating system storage pressure. Novus Life explicitly invokes:
```typescript
await navigator.storage.persist();
```
This transitions the storage sandbox to **persisted mode**, ensuring the database is exempted from automated OS purge mechanisms.

### 3.2 WebAPK Sandbox Isolation
On Android devices, the WebAPK packaging architecture assigns the application its own unique Linux User ID (UID), providing process isolation and restricting inter-process communication (IPC) to explicit system permissions.

---

## 4. Google Drive Integration Security

When backing up to Google Drive:
- Scope requested: `https://www.googleapis.com/auth/drive.appdata`.
- The application is sandboxed inside the hidden `appDataFolder`.
- The snapshot payload (`novus_life_vault.json.enc`) is encrypted with client-side AES-256-GCM before transmission. Google Drive servers receive only encrypted binary data.
