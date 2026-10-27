---
id: novus-life-api-reference
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 1.0.0-beta
title: Справочник REST API и руководство по интеграции Novus Life
description: Исчерпывающее руководство по REST API Novus Life, эндпоинты аутентификации, протокол дельта-синхронизации, облачный сейф Google Drive и AI-ассистент.
last_updated: '2026-10-27'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/API_REFERENCE.md
managed_by: sync_private_docs
---
# Справочник REST API и руководство по интеграции Novus Life

> **Версия:** 1.0.0-beta Enterprise Edition  
> **Базовый URL:** `https://novus-life.online/api` (Продакшен) или `http://localhost:3001/api` (Локальная разработка)  
> **Аутентификация:** Bearer Token (`Authorization: Bearer <JWT>`)  
> **OpenAPI 3.1 Контракт:** Доступен в [openapi.yaml](openapi.yaml) и [openapi.json](openapi.json)

---

## 1. Глобальные стандарты запросов и ответов

### Стандартные HTTP-заголовки
Все защищенные эндпоинты API требуют передачи следующих заголовков:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
```

### Стандартный формат ответов об ошибках
Все ошибки возвращаются в едином структурированном формате JSON:
```json
{
  "error": "Краткое понятное описание ошибки",
  "code": "INVALID_CREDENTIALS",
  "details": []
}
```

---

## 2. Диагностика и проверка состояния

### `GET /api/health`
Проверяет время непрерывной работы процесса бэкенда и статус пула подключений к PostgreSQL.

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
Создает новую учетную запись пользователя с криптографическим хэшированием пароля (`bcryptjs`).

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
Выполняет проверку учетных данных пользователя и выдает подписанный токен JWT.

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

## 4. Мультиарендная дельта-синхронизация (`/api/sync`)

Протокол синхронизации координирует состояние между клиентской базой IndexedDB (`Dexie.js`) и центральной базой данных PostgreSQL.

### `GET /api/sync`
Получает измененные записи по всем 12 таблицам предметных областей, начиная с переданной метки времени.

- **Аутентификация:** Требуется
- **Параметры запроса (Query Parameters):**
  - `since` *(string, ISO 8601)*: Метка времени последней успешной локальной синхронизации. Пример: `?since=2026-10-27T12:00:00.000Z`.
- **Ответ (`200 OK`):**
```json
{
  "serverTime": "2026-10-27T15:30:00.000Z",
  "addresses": [
    {
      "id": "0192e210-67a8-7d31-9f20-b44c20e18d09",
      "name": "Основная квартира",
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
Отправляет локально созданные или измененные записи на сервер с выполнением слияния (upsert).

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

## 5. Зашифрованный сейф Google Drive (`/api/drive`)

### `GET /api/drive/status`
Проверяет, авторизовал ли текущий пользователь личный сейф резервного копирования в Google Drive.

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
Загружает зашифрованный пакет JSON в изолированную скрытую системную папку пользователя `appDataFolder`.

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

## 6. Модуль AI-ассистента (`/api/gemini`)

### `POST /api/gemini/chat`
Обеспечивает интерактивный финансовый анализ и рекомендации по оптимизации тарифов с использованием Google Gemini API.

- **Аутентификация:** Требуется
- **Тело запроса:**
```json
{
  "message": "Как мне снизить счет за электричество при двухзонном тарифе день/ночь?",
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
  "reply": "По вашему двухзонному тарифу ночная электроэнергия на 50% дешевле с 23:00 до 07:00...",
  "suggestedActions": [
    "Настройте таймер бойлера на период с 23:00 до 06:00",
    "Запускайте стиральную и посудомоечную машины после 23:00"
  ]
}
```

---

## 7. HTTP-коды статусов и обработка ошибок

| Код | Статус | Значение |
| :---: | :--- | :--- |
| `200` | OK | Запрос успешно выполнен. |
| `201` | Created | Ресурс успешно создан. |
| `400` | Bad Request | Некорректный синтаксис JSON или неверные параметры. |
| `401` | Unauthorized | Отсутствует либо истек срок действия токена Bearer JWT. |
| `403` | Forbidden | Недостаточно прав согласно политикам Row Level Security. |
| `404` | Not Found | Запрашиваемая сущность не найдена. |
| `429` | Too Many Requests | Превышен лимит запросов (максимум 100 запросов / минуту). |
| `500` | Internal Server Error | Ошибка базы данных или неперехваченное исключение. |

---

*Для интерактивного тестирования импортируйте спецификацию [openapi.yaml](openapi.yaml) в Swagger Editor или Postman.*
