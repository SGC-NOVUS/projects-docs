---
id: novus-life-api-reference
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 1.0.0-beta
title: Довідник REST API та інструкція з інтеграції Novus Life
description: Вичерпний довідник з REST API Novus Life, ендпоінти автентифікації, протокол дельта-синхронізації, хмарний сейф Google Drive та модуль AI-асистента.
last_updated: '2026-10-27'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/API_REFERENCE.md
managed_by: sync_private_docs
---
# Довідник REST API та інструкція з інтеграції Novus Life

> **Версія:** 1.0.0-beta Enterprise Edition  
> **Базовий URL:** `https://novus-life.online/api` (Продакшен) або `http://localhost:3001/api` (Локальна розробка)  
> **Автентифікація:** Bearer Token (`Authorization: Bearer <JWT>`)  
> **OpenAPI 3.1 Контракт:** Доступний у [openapi.yaml](openapi.yaml) та [openapi.json](openapi.json)

---

## 1. Глобальні стандарти запитів та відповідей

### Стандартні HTTP-заголовки
Усі захищені ендпоінти API вимагають передачі наступних заголовків:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
```

### Стандартний формат відповідей про помилки
Усі помилки повертаються в єдиному уніфікованому форматі JSON:
```json
{
  "error": "Короткий зрозумілий опис помилки",
  "code": "INVALID_CREDENTIALS",
  "details": []
}
```

---

## 2. Діагностика та перевірка стану

### `GET /api/health`
Перевіряє час безперервної роботи процесу бекенда та стан пулу з'єднань з PostgreSQL.

- **Автентифікація:** Не потрібна (Публічний)
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

## 3. Автентифікація та керування обліковими записами (`/api/auth`)

### `POST /api/auth/register`
Створює новий обліковий запис користувача з криптографічним хешуванням пароля (`bcryptjs`).

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
Здійснює перевірку облікових даних користувача та видає підписаний токен JWT.

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
Повертає профіль поточного автентифікованого користувача.

- **Автентифікація:** Потрібна
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

## 4. Мультиорендна дельта-синхронізація (`/api/sync`)

Протокол синхронізації координує стан між клієнтською базою IndexedDB (`Dexie.js`) та центральною базою даних PostgreSQL.

### `GET /api/sync`
Отримує змінені записи з усіх 12 таблиць предметних областей, починаючи з переданої мітки часу.

- **Автентифікація:** Потрібна
- **Параметри запиту (Query Parameters):**
  - `since` *(string, ISO 8601)*: Мітка часу останньої успішної локальної синхронізації. Приклад: `?since=2026-10-27T12:00:00.000Z`.
- **Відповідь (`200 OK`):**
```json
{
  "serverTime": "2026-10-27T15:30:00.000Z",
  "addresses": [
    {
      "id": "0192e210-67a8-7d31-9f20-b44c20e18d09",
      "name": "Основна квартира",
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
Надсилає локально створені або змінені записи на сервер із виконанням злиття (upsert).

- **Автентифікація:** Потрібна
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

## 5. Зашифрований сейф Google Drive (`/api/drive`)

### `GET /api/drive/status`
Перевіряє, чи авторизував поточний користувач приватний сейф резервного копіювання у Google Drive.

- **Автентифікація:** Потрібна
- **Відповідь (`200 OK`):**
```json
{
  "isConnected": true,
  "lastBackupAt": "2026-10-26T22:00:00.000Z",
  "vaultFileId": "1a2b3c4d5e6f7g8h9i0j"
}
```

### `POST /api/drive/backup`
Завантажує зашифрований пакет JSON до ізольованої прихованої системної папки користувача `appDataFolder`.

- **Автентифікація:** Потрібна
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

## 6. Модуль AI-асистента (`/api/gemini`)

### `POST /api/gemini/chat`
Забезпечує інтерактивний фінансовий аналіз та рекомендації щодо оптимізації тарифів за допомогою Google Gemini API.

- **Автентифікація:** Потрібна
- **Тіло запиту:**
```json
{
  "message": "Як мені зменшити рахунок за електроенергію за двозонним тарифом день/ніч?",
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
  "reply": "За вашим двозонним тарифом нічна електроенергія на 50% дешевша з 23:00 до 07:00...",
  "suggestedActions": [
    "Налаштуйте таймер бойлера на період з 23:00 до 06:00",
    "Вмикайте пральну та посудомийну машини після 23:00"
  ]
}
```

---

## 7. HTTP-коди статусів та обробка помилок

| Код | Статус | Значення |
| :---: | :--- | :--- |
| `200` | OK | Запит успішно виконано. |
| `201` | Created | Ресурс успішно створено. |
| `400` | Bad Request | Некоректний синтаксис JSON або недійсні параметри. |
| `401` | Unauthorized | Відсутній або протермінований токен Bearer JWT. |
| `403` | Forbidden | Недостатньо прав згідно з політиками Row Level Security. |
| `404` | Not Found | Запитувану сутність не знайдено. |
| `429` | Too Many Requests | Перевищено ліміт запитів (максимум 100 запитів / хвилину). |
| `500` | Internal Server Error | Помилка бази даних або неперехоплене виключення. |

---

*Для інтерактивного тестування імпортуйте специфікацію [openapi.yaml](openapi.yaml) у Swagger Editor або Postman.*
