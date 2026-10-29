---
id: novus-life-api-reference
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: Novus Life — Довідник REST API та посібник з інтеграції
description: '> **Версія:** 1.0.0-beta Enterprise Edition > **Базовий URL:** https://novus-life.online/api
  (Production) або http://localhost:3001/api (Local Dev) > **Автентифікація:** Bearer
  Tok...'
last_updated: '2026-10-27'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/API_REFERENCE.md
managed_by: sync_private_docs
---
# Novus Life — Довідник з REST API та посібник з інтеграції

> **Версія:** 1.0.0-beta Enterprise Edition  
> **Базовий URL:** `https://novus-life.online/api` (Продакшн) або `http://localhost:3001/api` (Локальна розробка)  
> **Автентифікація:** Bearer Token (`Authorization: Bearer <JWT>`)  
> **Контракт OpenAPI 3.1:** Доступний у [openapi.yaml](openapi.yaml) та [openapi.json](openapi.json)

---

## 1. Глобальні стандарти запитів та відповідей

### Стандартні заголовки
Усі автентифіковані ендпоінти API вимагають наступних заголовків:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
```

### Стандартний формат відповіді з помилкою
```json
{
  "error": "Short human-readable error description",
  "code": "INVALID_CREDENTIALS",
  "details": []
}
```

---

## 2. Стан системи та діагностика

### `GET /api/health`
Перевіряє час безперервної роботи бекенд-процесу та стан пулу з'єднань PostgreSQL.

- **Автентифікація:** Відсутня (Публічний)
- **Відповідь (`200 OK`):**
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

## 3. Автентифікація та управління обліковими записами (`/api/auth`)

### `POST /api/auth/register`
Створює новий обліковий запис користувача з хешуванням пароля із сіллю (`bcryptjs`).

- **Тіло запиту:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "displayName": "Alex Doe"
}
```
- **Відповідь (`201 Created`):**
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
Автентифікує облікові дані користувача та видає підписаний JWT-токен.

- **Тіло запиту:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```
- **Відповідь (`200 OK`):**
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
Отримує профіль поточного автентифікованого користувача.

- **Автентифікація:** Обов'язкова
- **Відповідь (`200 OK`):**
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

## 4. Мультитенантна дельта-синхронізація (`/api/sync`)

Протокол синхронізації координує стан між клієнтською IndexedDB (`Dexie.js`) та основною базою даних PostgreSQL.

### `GET /api/sync`
Отримує змінені записи з усіх 12 доменних таблиць з моменту вказаної часової позначки.

- **Автентифікація:** Обов'язкова
- **Параметри запиту:**
  - `since` *(string, ISO 8601)*: Часова позначка останньої успішної локальної синхронізації. Приклад: `?since=2026-10-27T12:00:00.000Z`.
- **Відповідь (`200 OK`):**
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
Надсилає локально створені або змінені записи на сервер із злиттям upsert.

- **Автентифікація:** Обов'язкова
- **Тіло запиту:**
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
- **Відповідь (`200 OK`):**
```json
{
  "status": "success",
  "syncedAt": "2026-10-27T15:30:01.000Z",
  "rowsUpserted": 42
}
```

---

## 5. Зашифроване сховище Google Drive (`/api/drive`)

### `GET /api/drive/status`
Перевіряє, чи поточний користувач авторизував особисте сховище резервних копій Google Drive.

- **Автентифікація:** Обов'язкова
- **Відповідь (`200 OK`):**
```json
{
  "isConnected": true,
  "lastBackupAt": "2026-10-26T22:00:00.000Z",
  "vaultFileId": "1a2b3c4d5e6f7g8h9i0j"
}
```

### `POST /api/drive/backup`
Завантажує зашифрований JSON-payload в ізольовану `appDataFolder` користувача.

- **Автентифікація:** Обов'язкова
- **Тіло запиту:**
```json
{
  "encryptedData": "U2FsdGVkX19+...",
  "checksum": "a3b2c1..."
}
```
- **Відповідь (`200 OK`):**
```json
{
  "success": true,
  "uploadedAt": "2026-10-27T15:35:00.000Z"
}
```

---

## 6. Рушій AI-асистента (`/api/gemini`)

### `POST /api/gemini/chat`
Надає діалоговий фінансовий аналіз та поради щодо оптимізації тарифів за допомогою Google Gemini API.

- **Автентифікація:** Обов'язкова
- **Тіло запиту:**
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
- **Відповідь (`200 OK`):**
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

## 7. Коди стану HTTP та обробка помилок

| Код | Статус | Значення |
| :---: | :--- | :--- |
| `200` | OK | Запит виконано успішно. |
| `201` | Created | Ресурс успішно створено. |
| `400` | Bad Request | Неправильно сформоване тіло JSON або недійсний параметр. |
| `401` | Unauthorized | Відсутній або прострочений токен Bearer JWT. |
| `403` | Forbidden | Недостатньо прав у межах Row Level Security. |
| `404` | Not Found | Запитувана сутність не існує. |
| `429` | Too Many Requests | Перевищено ліміт запитів (макс. 100 запитів / хвилину). |
| `500` | Internal Server Error | Збій бази даних або необроблений виняток. |

---

*Для інтерактивного дослідження імпортуйте [openapi.yaml](openapi.yaml) у Swagger Editor або Postman.*
