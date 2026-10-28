---
id: novus-life-api-reference
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: Novus-Life — Справочник по REST API и руководство по интеграции
description: '> **Version:** 1.0.0-beta Enterprise Edition > **Base URL:** https://novus-life.online/api
  (Production) или http://localhost:3001/api (Local Dev) > **Authentication:** Bearer
  Tok...'
last_updated: '2026-10-27'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/API_REFERENCE.md
managed_by: sync_private_docs
---
# Novus-Life — Справочник по REST API и руководство по интеграции

> **Версия:** 1.0.0-beta Enterprise Edition  
> **Базовый URL:** `https://novus-life.online/api` (Production) или `http://localhost:3001/api` (Локальная разработка)  
> **Аутентификация:** Bearer Token (`Authorization: Bearer <JWT>`)  
> **Контракт OpenAPI 3.1:** Доступен в [openapi.yaml](openapi.yaml) и [openapi.json](openapi.json)

---

## 1. Глобальные стандарты запросов и ответов

### Стандартные заголовки
Для всех защищенных эндпоинтов API требуются следующие заголовки:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
```

### Стандартный формат ответа об ошибке
```json
{
  "error": "Short human-readable error description",
  "code": "INVALID_CREDENTIALS",
  "details": []
}
```

---

## 2. Работоспособность и диагностика

### `GET /api/health`
Проверяет время безотказной работы бэкенд-процесса и статус пула соединений PostgreSQL.

- **Аутентификация:** Не требуется (Публичный)
- **Ответ (`200 OK`):**
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

## 3. Аутентификация и управление учетными записями (`/api/auth`)

### `POST /api/auth/register`
Создает новую учетную запись пользователя с хешированием пароля с добавлением «соли» (`bcryptjs`).

- **Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "displayName": "Alex Doe"
}
```
- **Ответ (`201 Created`):**
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
Проверяет учетные данные пользователя и выдает подписанный JWT токен.

- **Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```
- **Ответ (`200 OK`):**
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
Возвращает профиль текущего аутентифицированного пользователя.

- **Аутентификация:** Требуется
- **Ответ (`200 OK`):**
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

## 4. Многопотоковая дельта-синхронизация (`/api/sync`)

Протокол синхронизации координирует состояние между клиентской IndexedDB (`Dexie.js`) и мастер-базой данных PostgreSQL.

### `GET /api/sync`
Получает измененные записи по всем 12 доменным таблицам с момента указанной временной метки.

- **Аутентификация:** Требуется
- **Параметры запроса:**
  - `since` *(строка, ISO 8601)*: Временная метка последней успешной локальной синхронизации. Пример: `?since=2026-10-27T12:00:00.000Z`.
- **Ответ (`200 OK`):**
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
Отправляет созданные или измененные локально записи на сервер с использованием слияния по принципу upsert.

- **Аутентификация:** Требуется
- **Тело запроса:**
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
- **Ответ (`200 OK`):**
```json
{
  "status": "success",
  "syncedAt": "2026-10-27T15:30:01.000Z",
  "rowsUpserted": 42
}
```

---

## 5. Зашифрованное хранилище Google Drive (`/api/drive`)

### `GET /api/drive/status`
Проверяет, авторизовал ли текущий пользователь персональное хранилище резервных копий на Google Drive.

- **Аутентификация:** Требуется
- **Ответ (`200 OK`):**
```json
{
  "isConnected": true,
  "lastBackupAt": "2026-10-26T22:00:00.000Z",
  "vaultFileId": "1a2b3c4d5e6f7g8h9i0j"
}
```

### `POST /api/drive/backup`
Загружает зашифрованный JSON-пакет в изолированную папку пользователя `appDataFolder`.

- **Аутентификация:** Требуется
- **Тело запроса:**
```json
{
  "encryptedData": "U2FsdGVkX19+...",
  "checksum": "a3b2c1..."
}
```
- **Ответ (`200 OK`):**
```json
{
  "success": true,
  "uploadedAt": "2026-10-27T15:35:00.000Z"
}
```

---

## 6. AI Assistant Engine (`/api/gemini`)

### `POST /api/gemini/chat`
Предоставляет интерактивный финансовый анализ и рекомендации по оптимизации тарифов с использованием Google Gemini API.

- **Аутентификация:** Требуется
- **Тело запроса:**
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
- **Ответ (`200 OK`):**
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

## 7. HTTP-статусы и обработка ошибок

| Код | Статус | Значение |
| :---: | :--- | :--- |
| `200` | OK | Запрос успешно выполнен. |
| `201` | Created | Ресурс успешно создан. |
| `400` | Bad Request | Некорректное тело JSON или неверный параметр. |
| `401` | Unauthorized | Отсутствует или истек срок действия Bearer JWT-токена. |
| `403` | Forbidden | Недостаточно прав в соответствии с Row Level Security. |
| `404` | Not Found | Запрашиваемая сущность не существует. |
| `429` | Too Many Requests | Превышен лимит запросов (максимум 100 запросов в минуту). |
| `500` | Internal Server Error | Сбой базы данных или необрабатываемое исключение. |

---

*Для интерактивного изучения импортируйте [openapi.yaml](openapi.yaml) в Swagger Editor или Postman.*
