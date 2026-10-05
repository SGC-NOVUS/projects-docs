# projects-docs

Public documentation repository for SGC-NOVUS.

## Principles
- English is the single source of truth (SSOT).
- Localized docs are generated automatically from English source documents.
- Documentation is published as content-as-code with predictable frontmatter.

## Repository Layout
- .github/workflows/auto-translate.yml
- catalog/docs-catalog-{locale}.json
- config/locales.json
- config/sources.json
- scripts/sync_private_docs.py
- scripts/translate.py
- scripts/export_catalog.py
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
5. Script automatically re-queues stale locale files (for example pending fallback or suspicious untranslated output).
6. Script generates `*.uk.md` and `*.ru.md` beside source files.
7. Workflow exports public static catalog JSON files in `catalog/`.
8. Workflow commits updated docs and catalog files.

Incremental translation mode:
- Workflow sets `TRANSLATION_MAX_DOCS_PER_RUN` (default `2`) to ensure each run finishes and commits progress.
- Pending locale files are prioritized first, then missing/stale locales.
- Set `TRANSLATION_MAX_DOCS_PER_RUN=0` for unlimited translation in one run.
- Completed fields and body chunks are checkpointed in `.tmp/translation-progress.json`. If every model is out of quota, the workflow saves those checkpoints and the next scheduled run resumes without retranslating completed chunks.
- Gemini request pacing reads each configured model's RPM, TPM, and RPD limits, tracks daily requests across workflow runs in `.tmp/gemini-usage.json`, and prefers models with more remaining daily capacity. API model input/output token limits are also checked before generation; RPM and TPM windows are paced rather than burst-called.
- Catalog export excludes pending, empty, untranslated, and materially incomplete RU/UK documents.
- Site import is held until both RU and UK catalogs contain validated translations for every English document, preventing an incomplete catalog from replacing the live database.

Public static catalog URL pattern:
- `https://raw.githubusercontent.com/SGC-NOVUS/projects-docs/main/catalog/docs-catalog-en.json`
- `https://raw.githubusercontent.com/SGC-NOVUS/projects-docs/main/catalog/docs-catalog-uk.json`
- `https://raw.githubusercontent.com/SGC-NOVUS/projects-docs/main/catalog/docs-catalog-ru.json`

## Private Source Sync

Source repositories and filters are configured in `config/sources.json`.

Default sources:
- `SGC-NOVUS/panel-core`
- `SGC-NOVUS/agent-core`
- `SGC-NOVUS/installer`

Optional product sources:
- `SGC-NOVUS/novus-edo` (cluster `novus-edo`)
- `SGC-NOVUS/novus-life` (cluster `novus-life`)

Optional sources can declare `optional: true` and `local_path` for local bootstrap import.
If unavailable in CI, they are skipped without failing the workflow.

Required secret:
- `DOCS_SYNC_GITHUB_TOKEN` (read access to private source repos)

English SSOT intake guard:
- Sync step imports only English source documents.
- Files detected as non-English are skipped and listed in `.tmp/source-sync-report.json` under `skipped_non_english`.

Selective local sync (only specific source keys):

```bash
DOCS_SYNC_LOCAL_ROOT=/opt/sgc-novus DOCS_SYNC_SOURCE_KEYS=novus-edo,novus-life python3 scripts/sync_private_docs.py
```

## Required GitHub Secrets

- `DOCS_SYNC_GITHUB_TOKEN` - token for cloning private repos.
- `GEMINI_API_KEY` - token for Gemini localization.
- `SITE_DOCS_SYNC_TOKEN` - authorizes importing generated catalogs into the public site's database.

## Gemini Cascade (Free Tier Friendly)

Localization uses a model cascade defined in `config/locales.json` under `gemini_model_cascade`.
If the current model is quota/rate exhausted (for example HTTP 429), the pipeline automatically
falls through to the next model in cascade order.

Current cascade:
| Model | RPM | TPM | RPD |
|---|---:|---:|---:|
| `gemini-3.8-flash` | 5 | 250,000 | 20 |
| `gemini-3.7-flash` | 5 | 250,000 | 20 |
| `gemini-3.6-flash` | 5 | 250,000 | 20 |
| `gemini-3.5-flash-lite` | 15 | 250,000 | 500 |
| `gemini-3.5-flash` | 5 | 250,000 | 20 |

The limits above are configured from the current AI Studio free-tier quota view and can change independently per project/model. `TPM` is the rolling token-throughput quota, not the model's maximum context window; context input/output limits are read from the Gemini model metadata API when available.

Localization failure policy:
- By default, the translator does **not** create new locale files with English fallback body.
- This prevents publishing `*.ru.md` / `*.uk.md` files that contain English text when Gemini is temporarily unavailable.
- Optional legacy behavior can be re-enabled with `TRANSLATION_ALLOW_PENDING_FALLBACK=true`.
- Workflow uses `cancel-in-progress: true` and a job timeout to avoid stale localization runs blocking newer fixes.
- If localization cannot finish, the workflow still commits completed translations and checkpoints, imports only validated catalog entries, then reports the run as failed so a later scheduled run can resume.

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
