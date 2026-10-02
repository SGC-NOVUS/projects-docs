# projects-docs

Public documentation repository for SGC-NOVUS.

## Principles
- English is the single source of truth (SSOT).
- Localized docs are generated automatically from English source documents.
- Documentation is published as content-as-code with predictable frontmatter.

## Repository Layout
- .github/workflows/auto-translate.yml
- config/locales.json
- config/sources.json
- scripts/sync_private_docs.py
- scripts/translate.py
- scripts/glossary.json
- content/{cluster}/{category}/{document}.{locale}.md

## Required Frontmatter for English Source Docs
Every `*.en.md` document must contain:
- id
- cluster
- category
- order
- status
- version
- title
- description
- last_updated

## Localization Flow
1. GitHub Actions syncs English docs from private repositories using `scripts/sync_private_docs.py`.
2. Script imports/updates English documents under `content/**` with strict frontmatter.
3. Workflow runs `scripts/translate.py` for changed English docs.
4. Script also backfills missing locale files for any existing English source docs.
5. Script generates `*.uk.md` and `*.ru.md` beside source files.
6. Workflow commits updated docs; public site consumes published repository content directly.

## Private Source Sync

Source repositories and filters are configured in `config/sources.json`.

Default sources:
- `SGC-NOVUS/panel-core`
- `SGC-NOVUS/agent-core`
- `SGC-NOVUS/installer`

Required secret:
- `DOCS_SYNC_GITHUB_TOKEN` (read access to private source repos)

English SSOT intake guard:
- Sync step imports only English source documents.
- Files detected as non-English are skipped and listed in `.tmp/source-sync-report.json` under `skipped_non_english`.

## Required GitHub Secrets

- `DOCS_SYNC_GITHUB_TOKEN` - token for cloning private repos.
- `GEMINI_API_KEY` - token for Gemini localization.

## Gemini Cascade (Free Tier Friendly)

Localization uses a model cascade defined in `config/locales.json` under `gemini_model_cascade`.
If the current model is quota/rate exhausted (for example HTTP 429), the pipeline automatically
falls through to the next model in cascade order.

Current cascade:
- `gemini-3.8-flash`
- `gemini-3.7-flash`
- `gemini-3.6-flash`
- `gemini-3.5-flash-lite`
- `gemini-3.5-flash`

Localization failure policy:
- By default, the translator does **not** create new locale files with English fallback body.
- This prevents publishing `*.ru.md` / `*.uk.md` files that contain English text when Gemini is temporarily unavailable.
- Optional legacy behavior can be re-enabled with `TRANSLATION_ALLOW_PENDING_FALLBACK=true`.

## Gemini Smoke Check

List configured cascade without API calls:

```bash
python3 scripts/smoke_gemini_cascade.py
```

Probe cascade until first successful model:

```bash
GEMINI_API_KEY=*** python3 scripts/smoke_gemini_cascade.py --probe
```

Probe all configured models:

```bash
GEMINI_API_KEY=*** python3 scripts/smoke_gemini_cascade.py --probe-all
```

Full localization rebuild (all English docs):

```bash
TRANSLATE_ALL=true GEMINI_API_KEY=*** python3 scripts/translate.py
```

In GitHub Actions, this can be triggered via manual `workflow_dispatch` input `translate_all=true`.
