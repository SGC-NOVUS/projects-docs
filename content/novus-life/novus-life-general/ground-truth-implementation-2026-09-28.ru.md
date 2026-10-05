---
id: novus-life-ground-truth-implementation-2026-09-28
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: 'Ground truth: реализация Novus-Life'
description: '**Status:** внутренний статический аудит чекаута от 2026-09-28. **Scope:**
  Vue/PWA routes, Express backend, PostgreSQL, Google integrations, email, browser
  storage и environm...'
last_updated: '2026-10-05'
source_locale: en
locale: ru
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/GROUND_TRUTH_IMPLEMENTATION_2026-09-28.md
managed_by: sync_private_docs
---
# Ground truth: Novus Life implementation

**Status:** внутренний статический аудит процесса оформления заказа от 2026-09-28.
**Scope:** Маршруты Vue/PWA, бэкенд на Express, PostgreSQL, интеграции с Google, почта, хранилище браузера и конфигурация окружения.

## Current architecture

Репозиторий не является шаблоном React, описанным в корневом файле README. Фактическая реализация:

| Layer | Actual implementation |
| --- | --- |
| Browser | Vue 3, Vite, Vue Router, Pinia, i18n и ресурсы PWA |
| Local client data | Службы хранения браузера / возможностей устройства и доменные сторы для адресов, услуг, тарифов, показаний счетчиков, платежей и напоминаний |
| API | Express на `0.0.0.0`, `PORT` по умолчанию `3001`; источник CORS — `*`; тела JSON/urlencoded ограничены до 15 МиБ |
| Persistence | PostgreSQL через пул `pg` Pool; сервер прекращает прослушивание после 10 неудачных попыток подключения с интервалом в 2 секунды |
| Identity | JWT по электронной почте/паролю плюс Google OAuth; время жизни bearer JWT составляет 60 дней |
| Cloud backup | Google Drive `appDataFolder`, принимающий непрозрачный зашифрованный полезный нагрузочный блок (payload) от клиента |
| Mail | Resend; отсутствие ключа API переключает почту на мок-объект логирования, который возвращает успех |

## Навигация в браузере и модули

| Область маршрута | Реализованные модули |
| --- | --- |
| Public | Landing, privacy, terms, about, auth |
| `/app` | Dashboard, profile, utilities, tariffs, addresses, services, payments, reminders, analytics, settings |
| Совместимость | Устаревшие короткие URL перенаправляются на `/app/*`; неизвестные пути перенаправляются на `/` |
| Поведение PWA | Лендинг перенаправляет на `/app` при запуске из автономного контекста / PWA |

Фронтенд-клиент API использует относительные вызовы same-origin, добавляет bearer token из `localStorage` и вызывает ошибку при ответах, отличных от 2xx (`src/core/services/api-client.ts`).

## Каталог API

| Префикс | Операции | Авторизация | Назначение |
| --- | --- | --- | --- |
| `/api/health` | `GET` | Нет | Данные о состоянии (health) процесса API |
| `/api/auth` | `POST /register`, `POST /login`, `GET /me`, `PUT /profile`, `POST /password/set`, `POST /password/change`, `POST /verify-email/request`, `GET /verify-email/confirm`, `GET /google/url`, `GET /google/callback`, `POST /google/exchange` | Смешанная; для profile, password и verify request требуется bearer token | Управление учетными записями, профилями, подтверждение email и Google OAuth |
| `/api/sync` | `GET /`, `POST /` | Bearer token | Восстановление и транзакционное обновление (upsert) адресов, услуг, тарифов, коммунальных услуг, регулярных платежей и напоминаний пользователя |
| `/api/drive` | `GET /status`, `POST /backup`, `GET /restore` | Bearer token | Сохранение и получение зашифрованных на стороне клиента резервных копий в Google Drive appDataFolder |

Сервер подключает эти группы в `server/src/index.ts`. Спецификация OpenAPI в репозитории отсутствует.

## Обеспечение персистентности и поведение при сбоях

`checkDbConnection()` выполняет повторные попытки `SELECT NOW()` десять раз и запускает аддитивные миграции `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` после успешного подключения. Неуспешная проверка базы данных завершает процесс до вызова `listen()`.

`POST /api/sync` оборачивает все операции upsert для таблиц в транзакцию PostgreSQL. При возникновении ошибки он выполняет `ROLLBACK`, возвращает код `500` и всегда освобождает клиент пула. API обрабатывает локальные ID на стороне клиента как входные данные, маппит их в значения UUIDv7 и заполняет пропущенные доменные поля значениями по умолчанию во время импорта.

Резервное копирование в Google Drive сохраняет переданный `encryptedPayload` как `novus_life_vault.json.enc` в скрытой папке пользователя `appDataFolder`; сервер не расшифровывает полезную нагрузку. Отсутствие refresh token приводит к возврату стандартного ответа «не подключено» / `400` в зависимости от эндпоинта. Ошибки OAuth отображаются как `500` при обмене токена и вызывают перенаправление с параметрами запроса ошибки в потоке обратного вызова (callback).

Запросы постоянного хранилища (persistent-storage) браузера выполняются по принципу best effort. Отклоненный запрос `navigator.storage.persist()` возвращается как результат с отсутствием персистентности, отображаемый для пользователя; он не блокирует работу приложения (`src/core/services/storage-manager.ts`).

## Реестр окружения

| Переменная | Тип/значение по умолчанию | Где используется | Критичность |
| --- | --- | --- | --- |
| `PORT` | целое число; `3001` | `server/src/index.ts` | Граница запуска |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `db`, `5432`, `novus_life`, `novus_user`, `novus_secret_pass_2026` | `server/src/db.ts` | **Критично** для персистентности в production; резервный пароль небезопасен |
| `JWT_SECRET` | секрет; `novus_life_default_jwt_secret_dev` | `server/src/auth.ts` | **Критично** для идентификации в production; при отсутствии используется небезопасное значение по умолчанию |
| `APP_URL` | URL; `https://novus-life.online` | Редиректы аутентификации и ссылки в email | Критично для функционала OAuth/ссылок в email |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | строки; пусто | Потоки Google OAuth и обновления токенов Drive | Критично только для функций Google |
| `RESEND_API_KEY` | секрет; пусто | Инициализация Resend | Критично для фактической доставки email; при отсутствии ключа включается заглушка логирования |
| `EMAIL_FROM_AUTH`, `EMAIL_FROM_NOTIFY`, `EMAIL_REPLY_TO` | строки отправителя со значениями продукта по умолчанию | `server/src/services/email.ts` | Критично только для брендинга/доставки email |
| `VITE_APP_NAME`, `VITE_APP_URL` | значения шаблона фронтенда | `.env.example` | В `src` не найдено текущих потребителей `import.meta.env` |
| `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` | значения шаблона фронтенда | `.env.example` | В `src` не найдено текущих потребителей `import.meta.env`; они не подтверждают активное использование рантайма Supabase |

`server/.env.example` существует и документирует переменные базы данных сервера, JWT, Google и email. Корневой `.env.example` документирует только Vite/Supabase/Google/email и не содержит бэкенд-переменные `PORT`, `DB_*`, `JWT_SECRET` и `APP_URL`; документация оператора должна указывать на шаблон сервера для развертывания бэкенда.

## Подтвержденные пробелы в документации

1. Замените корневой README React-шаблона на документацию Vue + Express + PostgreSQL.
2. Добавьте справочник API, сгенерированный из трех смонтированных маршрутизаторов Express.
3. Удалите небезопасные значения по умолчанию для JWT и пароля базы данных в production или сделайте так, чтобы запуск отклонял их вне режима разработки.
4. Уточните, что текущая клиентская синхронизация ориентирована на саморазворачиваемый Express API; значения Supabase в корневом шаблоне в настоящее время не используются кодом браузера.
