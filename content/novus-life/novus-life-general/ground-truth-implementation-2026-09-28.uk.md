---
id: novus-life-ground-truth-implementation-2026-09-28
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: 'Ground truth: реалізація Novus-Life'
description: '**Status:** внутрішній статичний аудит процесу оформлення замовлення
  (checkout) станом на 2026-09-28. **Scope:** маршрути Vue/PWA, бекенд на Express,
  PostgreSQL, інтеграції з Google, електронна пошта, сховище браузера та середовищ...'
last_updated: '2026-10-05'
source_locale: en
locale: uk
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/GROUND_TRUTH_IMPLEMENTATION_2026-09-28.md
managed_by: sync_private_docs
---
# Ground truth: Novus Life implementation

**Status:** внутрішній статичний аудит оформлення замовлення від 2026-09-28.
**Scope:** Vue/PWA routes, Express backend, PostgreSQL, Google integrations, email, browser storage and environment configuration.

## Current architecture

Репозиторій не є шаблоном React, описаним у його кореневому README. Відстежувана реалізація:

| Layer | Actual implementation |
| --- | --- |
| Browser | Vue 3, Vite, Vue Router, Pinia, i18n та PWA assets |
| Local client data | Browser storage/device capability services and domain stores for addresses, services, tariffs, meter readings, payments and reminders |
| API | Express на `0.0.0.0`, `PORT` за замовчуванням `3001`; CORS origin це `*`; тіла JSON/urlencoded обмежені до 15 MiB |
| Persistence | PostgreSQL через `pg` Pool; сервер відмовляється слухати після 10 невдалих спроб підключення з інтервалом у 2 секунди |
| Identity | Email/password JWT plus Google OAuth; час життя bearer JWT становить 60 днів |
| Cloud backup | Google Drive `appDataFolder`, receiving an opaque encrypted payload from the client |
| Mail | Resend; відсутність API-ключа перемикає пошту на макет логування, який повертає успіх |

## Навігація браузера та модулі

| Область маршруту | Реалізовані модулі |
| --- | --- |
| Public | Landing, privacy, terms, about, auth |
| `/app` | Dashboard, profile, utilities, tariffs, addresses, services, payments, reminders, analytics, settings |
| Сумісність | Застарілі короткі URL-адреси перенаправляють на `/app/*`; невідомі шляхи перенаправляють на `/` |
| Поведінка PWA | Landing перенаправляє на `/app` при запуску з автономного контексту / PWA |

Клієнтський API-клієнт використовує відносні виклики same-origin, додає bearer token із `localStorage` та викидає виняток для відповідей, відмінних від 2xx (`src/core/services/api-client.ts`).

## Каталог API

| Префікс | Операції | Автентифікація | Призначення |
| --- | --- | --- | --- |
| `/api/health` | `GET` | Ні | Корисне навантаження стану процесу API |
| `/api/auth` | `POST /register`, `POST /login`, `GET /me`, `PUT /profile`, `POST /password/set`, `POST /password/change`, `POST /verify-email/request`, `GET /verify-email/confirm`, `GET /google/url`, `GET /google/callback`, `POST /google/exchange` | Змішана; профіль/пароль/запит підтвердження вимагають bearer token | Ідентифікація, профіль, підтвердження електронної пошти та Google OAuth |
| `/api/sync` | `GET /`, `POST /` | Bearer token | Відновлення та транзакційне оновлення/вставка (upsert) адреסים користувача, послуг, тарифів, комунальних послуг, регулярних платежів і нагадувань |
| `/api/drive` | `GET /status`, `POST /backup`, `GET /restore` | Bearer token | Зберігання/отримання зашифрованого на клієнті резервного копіювання в Google Drive appDataFolder |

Сервер монтує ці групи в `server/src/index.ts`. У репозиторії немає специфікації OpenAPI 3.1.

## Персистентність та поведінка у разі збоїв

`checkDbConnection()` повторює спробу виконання `SELECT NOW()` десять разів і виконує аддитивні міграції `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` після успішного з'єднання. Невдала перевірка бази даних завершує процес перед викликом `listen()`.

`POST /api/sync` загортає всі операції upsert для таблиць у транзакцію PostgreSQL. У разі помилки вона виконує `ROLLBACK`, повертає `500` і завжди звільняє клієнта пулу. API обробляє локальні ідентифікатори клієнтської сторони як вхідні дані, мапує їх на значення UUIDv7 та заповнює відсутні доменні поля за замовчуванням під час імпорту.

Резервне копіювання Google Drive зберігає наданий `encryptedPayload` як `novus_life_vault.json.enc` у прихованій пачці користувача `appDataFolder`; сервер не розшифровує цей корисний навантаження (payload). Відсутність токена оновлення (refresh token) повертає звичайну відповідь "not connected" / `500` залежно від ендпоінту. Збої OAuth проявляються як `500` під час обміну та перенаправляють з параметрами запиту помилки у потоці зворотного виклику (callback flow).

Запити на постійне зберігання у браузері (persistent-storage) виконуються за принципом «найкращих зусиль» (best effort). Відхилений запит `navigator.storage.persist()` повертається як результат для користувача про те, що сховище не є постійним; він не блокує застосунок (`src/core/services/storage-manager.ts`).

## Реєстр середовища

| Змінна | Тип/значення за замовчуванням | Де використовується | Критичність |
| --- | --- | --- | --- |
| `PORT` | ціле число; `3001` | `server/src/index.ts` | Межа запуску |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `db`, `5432`, `novus_life`, `novus_user`, `novus_secret_pass_2026` | `server/src/db.ts` | **Критично** для персистентності у прод-середовищі; резервний пароль є небезпечним |
| `JWT_SECRET` | секрет; `novus_life_default_jwt_secret_dev` | `server/src/auth.ts` | **Критично** для ідентифікації у прод-середовищі; небезпечне резервне значення активне, якщо пропущено |
| `APP_URL` | URL; `https://novus-life.online` | Перенаправлення автентифікації та посилання в електронних листах | Критично для функціоналу OAuth/посилань у пошті |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | рядки; порожньо | Потоки оновлення Google OAuth та Drive | Критично лише для функцій Google |
| `RESEND_API_KEY` | секрет; порожньо | Ініціалізація Resend | Критично для фактичної доставки пошти; відсутній ключ активує імітацію логування |
| `EMAIL_FROM_AUTH`, `EMAIL_FROM_NOTIFY`, `EMAIL_REPLY_TO` | рядки відправника зі значеннями продукту за замовчуванням | `server/src/services/email.ts` | Критично лише для брендування/доставки електронної пошти |
| `VITE_APP_NAME`, `VITE_APP_URL` | значення шаблону фронтенду | `.env.example` | Не знайдено жодного поточного споживача `import.meta.env` у `src` |
| `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` | значення шаблону фронтенду | `.env.example` | Не знайдено жодного поточного споживача `import.meta.env` у `src`; вони не є свідченням активного використання середовища виконання Supabase |

`server/.env.example` існує та документує значення бази даних сервера, JWT, Google та електронної пошти. Кореневий файл `.env.example` документує лише Vite/Supabase/Google/email і пропускає змінні бекенду `PORT`, `DB_*`, `JWT_SECRET` та `APP_URL`; документація для оператора має вказувати на шаблон сервера для розгортання бекенду.

## Підтверджені прогалини в документації

1. Замінити README кореневого шаблону React на документацію для Vue + Express + PostgreSQL.
2. Додати довідник API, згенерований з трьох підключених маршрутизаторів Express.
3. Видалити незахищені значення за замовчуванням для продакшну для JWT і пароля бази даних, або налаштувати відхилення при запуску поза середовищем розробки.
4. Уточнити, що поточна синхронізація клієнта спрямована на self-hosted Express API; значення Supabase в кореневому шаблоні наразі не використовуються кодом браузера.
