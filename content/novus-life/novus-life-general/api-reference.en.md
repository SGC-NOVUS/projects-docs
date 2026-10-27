---
id: novus-life-api-reference
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: Novus Life — REST API Reference & Integration Guide
description: '> **Version:** 1.0.0-beta Enterprise Edition > **Base URL:** https://novus-life.online/api
  (Production) or http://localhost:3001/api (Local Dev) > **Authentication:** Bearer
  Tok...'
last_updated: '2026-10-27'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/API_REFERENCE.md
managed_by: sync_private_docs
---
# Novus Life — REST API Reference & Integration Guide

> **Version:** 1.0.0-beta Enterprise Edition  
> **Base URL:** `https://novus-life.online/api` (Production) or `http://localhost:3001/api` (Local Dev)  
> **Authentication:** Bearer Token (`Authorization: Bearer <JWT>`)  
> **OpenAPI 3.1 Contract:** Available in [openapi.yaml](openapi.yaml) and [openapi.json](openapi.json)

---

## 1. Global Request & Response Standards

### Standard Headers
All authenticated API endpoints require the following headers:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
```

### Standard Error Response Format
```json
{
  "error": "Short human-readable error description",
  "code": "INVALID_CREDENTIALS",
  "details": []
}
```

---

## 2. Health & Diagnostics

### `GET /api/health`
Checks backend process uptime and PostgreSQL connection pool status.

- **Authentication:** None (Public)
- **Response (`200 OK`):**
```json
{
  "status": "healthy",
  "timestamp": "2026-10-27T15:00:00.000Z",
  "version": "1.0.0-beta",
  "database": "connected",
  "uptimeSeconds": 86400
}
```

---

## 3. Authentication & Account Management (`/api/auth`)

### `POST /api/auth/register`
Creates a new user account with salted password hashing (`bcryptjs`).

- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "displayName": "Alex Doe"
}
```
- **Response (`201 Created`):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "0192e210-67a8-7d31-9f20-b44c20e18d09",
    "email": "user@example.com",
    "displayName": "Alex Doe",
    "isVerified": false,
    "createdAt": "2026-10-27T15:00:00.000Z"
  }
}
```

### `POST /api/auth/login`
Authenticates user credentials and issues a signed JWT token.

- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```
- **Response (`200 OK`):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "0192e210-67a8-7d31-9f20-b44c20e18d09",
    "email": "user@example.com",
    "displayName": "Alex Doe"
  }
}
```

### `GET /api/auth/me`
Retrieves the profile of the currently authenticated user.

- **Authentication:** Required
- **Response (`200 OK`):**
```json
{
  "id": "0192e210-67a8-7d31-9f20-b44c20e18d09",
  "email": "user@example.com",
  "displayName": "Alex Doe",
  "familyId": "0192e215-4fa2-7b21-8b10-e75b92f91a14",
  "isVerified": true
}
```

---

## 4. Multi-Tenant Delta Synchronization (`/api/sync`)

The synchronization protocol coordinates state between client IndexedDB (`Dexie.js`) and the master PostgreSQL database.

### `GET /api/sync`
Retrieves modified records across all 12 domain tables since the provided timestamp.

- **Authentication:** Required
- **Query Parameters:**
  - `since` *(string, ISO 8601)*: Timestamp of last successful local sync. Example: `?since=2026-10-27T12:00:00.000Z`.
- **Response (`200 OK`):**
```json
{
  "serverTime": "2026-10-27T15:30:00.000Z",
  "addresses": [
    {
      "id": "0192e210-67a8-7d31-9f20-b44c20e18d09",
      "name": "Main Apartment",
      "color": "#6366f1",
      "area": 75.5,
      "residentsCount": 3,
      "valuta": "USD",
      "updatedAt": "2026-10-27T14:15:00.000Z"
    }
  ],
  "services": [],
  "tariffs": [],
  "utilities": [],
  "payments": [],
  "reminders": [],
  "schedules": [],
  "shifts": [],
  "financialAccounts": [],
  "financialTransactions": [],
  "budgetCategories": [],
  "piggyBanks": []
}
```

### `POST /api/sync`
Pushes locally created or modified records to the server with upsert merge.

- **Authentication:** Required
- **Request Body:**
```json
{
  "clientTime": "2026-10-27T15:30:00.000Z",
  "addresses": [ ... ],
  "services": [ ... ],
  "tariffs": [ ... ],
  "utilities": [ ... ],
  "payments": [ ... ],
  "reminders": [ ... ],
  "schedules": [ ... ],
  "shifts": [ ... ],
  "financialAccounts": [ ... ],
  "financialTransactions": [ ... ],
  "budgetCategories": [ ... ],
  "piggyBanks": [ ... ]
}
```
- **Response (`200 OK`):**
```json
{
  "status": "success",
  "syncedAt": "2026-10-27T15:30:01.000Z",
  "rowsUpserted": 42
}
```

---

## 5. Google Drive Encrypted Vault (`/api/drive`)

### `GET /api/drive/status`
Checks if the current user has authorized a personal Google Drive backup vault.

- **Authentication:** Required
- **Response (`200 OK`):**
```json
{
  "isConnected": true,
  "lastBackupAt": "2026-10-26T22:00:00.000Z",
  "vaultFileId": "1a2b3c4d5e6f7g8h9i0j"
}
```

### `POST /api/drive/backup`
Uploads an encrypted JSON payload into the user's isolated `appDataFolder`.

- **Authentication:** Required
- **Request Body:**
```json
{
  "encryptedData": "U2FsdGVkX19+...",
  "checksum": "a3b2c1..."
}
```
- **Response (`200 OK`):**
```json
{
  "success": true,
  "uploadedAt": "2026-10-27T15:35:00.000Z"
}
```

---

## 6. AI Assistant Engine (`/api/gemini`)

### `POST /api/gemini/chat`
Provides conversational financial analysis and tariff optimization advice using Google Gemini API.

- **Authentication:** Required
- **Request Body:**
```json
{
  "message": "How can I reduce my electric bill under a 2-tier day/night tariff?",
  "context": {
    "currentTariff": "two_tier",
    "dayRate": 4.32,
    "nightRate": 2.16
  }
}
```
- **Response (`200 OK`):**
```json
{
  "reply": "Under your two-tier tariff, night electricity is 50% cheaper between 23:00 and 07:00...",
  "suggestedActions": [
    "Schedule water heater timer between 23:00 and 06:00",
    "Run washing machine after 23:00"
  ]
}
```

---

## 7. HTTP Status Codes & Error Handling

| Code | Status | Meaning |
| :---: | :--- | :--- |
| `200` | OK | Request succeeded. |
| `201` | Created | Resource successfully created. |
| `400` | Bad Request | Malformed JSON body or invalid parameter. |
| `401` | Unauthorized | Missing or expired Bearer JWT token. |
| `403` | Forbidden | Insufficient permissions under Row Level Security. |
| `404` | Not Found | Requested entity does not exist. |
| `429` | Too Many Requests | Rate limit exceeded (Max 100 requests / minute). |
| `500` | Internal Server Error | Database failure or unhandled exception. |

---

*For interactive exploration, import [openapi.yaml](openapi.yaml) into Swagger Editor or Postman.*
