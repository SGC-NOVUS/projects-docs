---
id: novus-life-ground-truth-implementation-2026-09-28
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: 'Ground truth: реализация Novus-Life'
description: '**Status:** внутренний статический аудит оформления заказа от 2026-09-28.
  **Scope:** маршруты Vue/PWA, бэкенд Express, PostgreSQL, интеграции Google, email,
  браузерное хранилище и окруж...'
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/GROUND_TRUTH_IMPLEMENTATION_2026-09-28.md
managed_by: sync_private_docs
---
# Ground truth: Novus Life implementation

**Status:** внутренний статический аудит процесса оформления заказа от 28.09.2026.
**Scope:** маршруты Vue/PWA, бэкенд на Express, PostgreSQL, интеграции с Google, электронная почта, хранилище браузера и конфигурация окружения.

## Current architecture

Репозиторий не является шаблоном React, описанным в его корневом README. Фактическая реализация представляет собой:

| Layer | Actual implementation |
| --- | --- |
| Browser | Vue 3, Vite, Vue Router, Pinia, i18n и PWA-ассеты |
| Local client data | Сервисы хранилища браузера / возможностей устройства и доменные сторы для адресов, услуг, тарифов, показаний счетчиков, платежей и напоминаний |
| API | Express на `0.0.0.0`, порт по умолчанию `3001`; источником CORS является `*`; тела запросов JSON/urlencoded ограничены до 15 МиБ |
| Persistence | PostgreSQL через пул `pg` Pool; сервер прекращает прослушивание после 10 неудачных попыток подключения с интервалом в 2 секунды |
| Identity | JWT по электронной почте/паролю плюс Google OAuth; время жизни JWT типа bearer составляет 60 дней |
| Cloud backup | Google Drive `appDataFolder`, получающий непрозрачный зашифрованный полезный нагрузочный блок (payload) от клиента |
| Mail | Resend; отсутствие ключа API переключает отправку почты на заглушку с логированием, которая возвращает успех |

## Навигация в браузере и модули

| Область маршрута | Реализованные модули |
| --- | --- |
| Public | Landing, privacy, terms, about, auth |
| `/app` | Dashboard, profile, utilities, tariffs, addresses, services, payments, reminders, analytics, settings |
| Compatibility | Устаревшие короткие URL перенаправляются на `/app/*`; неизвестные пути перенаправляются на `/` |
| PWA behavior | Лендинг перенаправляется на `/app` при запуске из автономного контекста / PWA |

Фронтенд-клиент API использует относительные вызовы same-origin, добавляет bearer token из `localStorage` и генерирует исключение при ответах, отличных от 2xx (`src/core/services/api-client.ts`).

## Каталог API

| Префикс | Операции | Аутентификация | Назначение |
| --- | --- | --- | --- |
| `/api/health` | `GET` | Нет | Данные о состоянии процесса API |
| `/api/auth` | `POST /register`, `POST /login`, `GET /me`, `PUT /profile`, `POST /password/set`, `POST /password/change`, `POST /verify-email/request`, `GET /verify-email/confirm`, `GET /google/url`, `GET /google/callback`, `POST /google/exchange` | Смешанная; для профиля, пароля и запроса верификации требуется bearer token | Идентификация, профиль, верификация электронной почты и Google OAuth |
| `/api/sync` | `GET /`, `POST /` | Bearer token | Восстановление и транзакционное обновление/вставка (upsert) адресов, услуг, тарифов, коммунальных услуг, регулярных платежей и напоминаний пользователя |
| `/api/drive` | `GET /status`, `POST /backup`, `GET /restore` | Bearer token | Сохранение/получение зашифрованного на стороне клиента резервного копирования в appDataFolder Google Drive |

Сервер подключает эти группы в `server/src/index.ts`. В репозитории отсутствует спецификация OpenAPI.

## Обеспечение персистентности и поведение при сбоях

`checkDbConnection()` выполняет повторные попытки `SELECT NOW()` десять раз и запускает аддитивные миграции `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` после успешного подключения. Неуспешная проверка базы данных завершает процесс до вызова `listen()`.

`POST /api/sync` оборачивает все операции upsert для таблиц в транзакцию PostgreSQL. При возникновении ошибки он выполняет `ROLLBACK`, возвращает код `500` и всегда освобождает клиент пула. API обрабатывает локальные идентификаторы на стороне клиента как входные данные, сопоставляет их со значениями UUIDv7 и заполняет недостающие поля предметной области значениями по умолчанию во время импорта.

Резервное копирование в Google Drive сохраняет переданный `encryptedPayload` как `novus_life_vault.json.enc` в скрытой папке пользователя `appDataFolder`; сервер не расшифровывает полезную нагрузку. Отсутствие токена обновления возвращает обычный ответ "не подключено"/`400` в зависимости от эндпоинта. Ошибки OAuth отображаются как `500` при обмене и перенаправляются с параметрами запроса ошибки в потоке обратного вызова (callback).

Запросы постоянного хранилища браузера выполняются по принципу "лучших усилий" (best effort). Отклоненный запрос `navigator.storage.persist()` возвращается как результат без постоянного хранения, видимый пользователю; он не блокирует работу приложения (`src/core/services/storage-manager.ts`).

## Реестр переменных окружения

| Переменная | Тип/значение по умолчанию | Где используется | Критичность |
| --- | --- | --- | --- |
| `PORT` | целое число; `3001` | `server/src/index.ts` | Граница запуска |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `db`, `5432`, `novus_life`, `novus_user`, `novus_secret_pass_2026` | `server/src/db.ts` | **Критично** для персистентности в продакшене; резервный пароль небезопасен |
| `JWT_SECRET` | секрет; `novus_life_default_jwt_secret_dev` | `server/src/auth.ts` | **Критично** для идентификации в продакшене; если опущено, активен небезопасный резервный вариант |
| `APP_URL` | URL; `https://novus-life.online` | Перенаправления авторизации и ссылки в email | Критично для функционала OAuth/ссылок в email |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | строки; пусто | Процессы обновления токенов Google OAuth и Drive | Критично для функционала Google |
| `RESEND_API_KEY` | секрет; пусто | Инициализация Resend | Критично для фактической отправки email; отсутствие ключа включает мок-логирование |
| `EMAIL_FROM_AUTH`, `EMAIL_FROM_NOTIFY`, `EMAIL_REPLY_TO` | строки отправителя со значениями продукта по умолчанию | `server/src/services/email.ts` | Критично только для брендинга/доставки email |
| `VITE_APP_NAME`, `VITE_APP_URL` | значения шаблона фронтенда | `.env.example` | В `src` не найдено текущих потребителей `import.meta.env` |
| `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` | значения шаблона фронтенда | `.env.example` | В `src` не найдено текущих потребителей `import.meta.env`; они не свидетельствуют об активном использовании рантайма Supabase |

`server/.env.example` существует и документирует переменные базы данных сервера, JWT, Google и email. Корневой `.env.example` документирует только Vite/Supabase/Google/email и не включает бэкендные `PORT`, `DB_*`, `JWT_SECRET` и `APP_URL`; документация для операторов должна указывать на шаблон сервера для развертывания бэкенда.

## Подтвержденные пробелы в документации

1. Замените README корневого React-шаблона на документацию по Vue + Express + PostgreSQL.
2. Добавьте справочник по API, сгенерированный из трех подключенных роутеров Express.
3. Удалите небезопасные значения по умолчанию для JWT и пароля базы данных, используемые в production, либо сделайте так, чтобы при запуске они отклонялись вне режима разработки.
4. Уточните, что текущая синхронизация клиентов ориентирована на self-hosted API на базе Express; значения Supabase в корневом шаблоне в настоящее время не используются кодом в браузере.
