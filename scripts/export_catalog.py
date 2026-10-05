#!/usr/bin/env python3
"""
Export docs catalog JSON files for public static consumption.

Outputs:
- catalog/docs-catalog-en.json
- catalog/docs-catalog-uk.json
- catalog/docs-catalog-ru.json
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from typing import Dict, List, Tuple

import yaml

from translate import is_translation_suspicious

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
CATALOG_DIR = ROOT / "catalog"
LOCALES = ("en", "uk", "ru")


@dataclass
class DocRecord:
    article_id: str
    slug: str
    locale: str
    cluster: str
    category: str
    sort_order: int
    status: str
    version: str
    title: str
    description: str
    last_updated: str | None
    content_markdown: str
    source_path: str


def parse_markdown(path: pathlib.Path) -> Tuple[Dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text.strip()

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text.strip()

    fm_raw = parts[0][4:]
    body = parts[1]
    frontmatter = yaml.safe_load(fm_raw) or {}
    if not isinstance(frontmatter, dict):
        frontmatter = {}

    return frontmatter, body.strip()


def infer_slug(path: pathlib.Path, locale: str) -> str:
    suffix = f".{locale}.md"
    name = path.name
    if name.endswith(suffix):
        return name[: -len(suffix)]
    return path.stem


def as_int(value: object, default: int = 100) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return default


def as_text(value: object, default: str = "") -> str:
    text = str(value or "").strip()
    return text if text else default


def collect_locale(locale: str) -> List[DocRecord]:
    docs: List[DocRecord] = []
    rejected = 0
    for path in sorted(CONTENT_DIR.rglob(f"*.{locale}.md")):
        fm, body = parse_markdown(path)
        rel = path.relative_to(ROOT).as_posix()

        slug = infer_slug(path, locale)
        if locale != "en":
            source_path = path.with_name(path.name[: -len(f".{locale}.md")] + ".en.md")
            if not source_path.is_file():
                print(f"skipped {rel}: missing English source")
                rejected += 1
                continue

            source_fm, source_body = parse_markdown(source_path)
            translation_status = as_text(fm.get("translation_status"), "").lower()
            source_locale = as_text(fm.get("source_locale"), "en").lower()
            document_locale = as_text(fm.get("locale"), locale).lower()
            localized_title = as_text(fm.get("title"))
            localized_description = as_text(fm.get("description"))
            invalid_reason = ""
            if translation_status == "pending":
                invalid_reason = "translation is marked pending"
            elif source_locale != "en" or document_locale != locale:
                invalid_reason = "locale metadata does not match the catalog"
            elif not localized_title or not localized_description or not body.strip():
                invalid_reason = "localized title, description, or body is empty"
            elif is_translation_suspicious(
                as_text(source_fm.get("title")),
                localized_title,
                locale,
                "title",
            ):
                invalid_reason = "title appears untranslated"
            elif is_translation_suspicious(
                as_text(source_fm.get("description")),
                localized_description,
                locale,
                "description",
            ):
                invalid_reason = "description appears untranslated"
            elif is_translation_suspicious(source_body, body, locale, "body"):
                invalid_reason = "body appears untranslated or incomplete"

            if invalid_reason:
                print(f"skipped {rel}: {invalid_reason}")
                rejected += 1
                continue

        cluster = as_text(fm.get("cluster"), "documentation")
        category = as_text(fm.get("category"), "general")
        title = as_text(fm.get("title"), slug)
        description = as_text(fm.get("description"), "")
        status = as_text(fm.get("status"), "active")
        version = as_text(fm.get("version"), "")
        article_id = as_text(fm.get("id"), slug)
        source_path = as_text(fm.get("source_path"), rel)
        last_updated = as_text(fm.get("last_updated"), "")
        sort_order = as_int(fm.get("order"), 100)

        docs.append(
            DocRecord(
                article_id=article_id,
                slug=slug,
                locale=locale,
                cluster=cluster,
                category=category,
                sort_order=sort_order,
                status=status,
                version=version,
                title=title,
                description=description,
                last_updated=last_updated or None,
                content_markdown=body,
                source_path=source_path,
            )
        )

    docs.sort(key=lambda d: (d.cluster, d.category, d.sort_order, d.slug))
    if locale != "en":
        print(f"validated {locale} catalog: {len(docs)} accepted, {rejected} rejected")
    return docs


def write_catalog(locale: str, docs: List[DocRecord]) -> pathlib.Path:
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CATALOG_DIR / f"docs-catalog-{locale}.json"

    payload = {
        "ok": True,
        "locale": locale,
        "documents": [
            {
                "article_id": d.article_id,
                "slug": d.slug,
                "locale": d.locale,
                "cluster": d.cluster,
                "category": d.category,
                "sort_order": d.sort_order,
                "status": d.status,
                "version": d.version,
                "title": d.title,
                "description": d.description,
                "last_updated": d.last_updated,
                "content_markdown": d.content_markdown,
                "source_path": d.source_path,
            }
            for d in docs
        ],
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out_path


def main() -> int:
    generated: List[pathlib.Path] = []
    for locale in LOCALES:
        docs = collect_locale(locale)
        out = write_catalog(locale, docs)
        generated.append(out)
        print(f"generated: {out.relative_to(ROOT).as_posix()} ({len(docs)} docs)")

    (ROOT / ".tmp").mkdir(parents=True, exist_ok=True)
    (ROOT / ".tmp" / "catalog-files.txt").write_text(
        "\n".join(p.relative_to(ROOT).as_posix() for p in generated) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
