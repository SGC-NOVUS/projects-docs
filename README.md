# sgc-novus-docs

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
4. Script generates `*.uk.md` and `*.ru.md` beside source files.
5. Workflow commits updated docs and sends sync webhook.

## Private Source Sync

Source repositories and filters are configured in `config/sources.json`.

Default sources:
- `SGC-NOVUS/panel-core`
- `SGC-NOVUS/agent-core`
- `SGC-NOVUS/installer`

Required secret:
- `DOCS_SYNC_GITHUB_TOKEN` (read access to private source repos)

## Required GitHub Secrets

- `DOCS_SYNC_GITHUB_TOKEN` - token for cloning private repos.
- `GEMINI_API_KEY` - token for Gemini localization.
- `DOCS_SYNC_WEBHOOK_URL` (optional) - portal sync webhook endpoint.
- `DOCS_SYNC_WEBHOOK_SECRET` (optional) - HMAC secret for webhook signature.
