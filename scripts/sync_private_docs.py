#!/usr/bin/env python3
"""
Sync English documentation from private SGC-NOVUS repositories.

- Clones configured private repositories using DOCS_SYNC_GITHUB_TOKEN.
- Imports selected markdown sources into content/{cluster}/{category}/{document}.en.md.
- Generates strict frontmatter when source files don't have it.
- Keeps managed documents in sync and removes stale managed files.
"""

from __future__ import annotations

import datetime as dt
import fnmatch
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
TMP_DIR = ROOT / ".tmp"
SOURCES_CONFIG = ROOT / "config" / "sources.json"

REQUIRED_FRONTMATTER = {
    "id",
    "cluster",
    "category",
    "order",
    "status",
    "version",
    "title",
    "description",
    "last_updated",
}


@dataclass
class SourceSpec:
    repo: str
    branch: str
    repo_key: str
    cluster: str
    include_globs: List[str]
    exclude_globs: List[str]
    local_path: str
    optional: bool


def run(cmd: List[str], cwd: pathlib.Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def load_sources(path: pathlib.Path) -> Tuple[str, List[SourceSpec]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    default_version = str(data.get("default_version", "0.1.0"))
    sources_raw = data.get("sources", [])
    if not isinstance(sources_raw, list) or not sources_raw:
        raise RuntimeError("config/sources.json must contain non-empty 'sources' array")

    sources: List[SourceSpec] = []
    for idx, item in enumerate(sources_raw):
        if not isinstance(item, dict):
            raise RuntimeError(f"sources[{idx}] must be object")

        include = item.get("include_globs", ["docs/**/*.md"])
        exclude = item.get("exclude_globs", [])
        if not isinstance(include, list) or not all(isinstance(x, str) for x in include):
            raise RuntimeError(f"sources[{idx}].include_globs must be string list")
        if not isinstance(exclude, list) or not all(isinstance(x, str) for x in exclude):
            raise RuntimeError(f"sources[{idx}].exclude_globs must be string list")

        sources.append(
            SourceSpec(
                repo=str(item.get("repo", "")).strip(),
                branch=str(item.get("branch", "main")).strip() or "main",
                repo_key=str(item.get("repo_key", "")).strip(),
                cluster=str(item.get("cluster", "novus-os")).strip() or "novus-os",
                include_globs=include,
                exclude_globs=exclude,
                local_path=str(item.get("local_path", "")).strip(),
                optional=bool(item.get("optional", False)),
            )
        )

    for idx, src in enumerate(sources):
        if not src.repo or "/" not in src.repo:
            raise RuntimeError(f"sources[{idx}].repo must be like 'org/repo'")
        if not src.repo_key:
            raise RuntimeError(f"sources[{idx}].repo_key is required")

    return default_version, sources


def parse_markdown_doc(text: str) -> Tuple[Dict[str, object], str]:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            fm_raw = parts[0][4:]
            frontmatter = yaml.safe_load(fm_raw) or {}
            if isinstance(frontmatter, dict):
                return frontmatter, parts[1]
    return {}, text


def is_probably_non_english(text: str) -> bool:
    """
    Heuristic language guard for English SSOT intake.
    Skips documents that are clearly Cyrillic-dominant.
    """
    cyr = len(re.findall(r"[А-Яа-яЁёІЇЄієїґҐ]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if cyr < 40:
        return False
    if latin == 0:
        return True
    # If Cyrillic is a meaningful share of prose, keep it out of EN SSOT.
    return (cyr / latin) >= 0.15


def dump_markdown_doc(frontmatter: Dict[str, object], body: str) -> str:
    fm = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{fm}\n---\n{body.strip()}\n"


def slugify(value: str) -> str:
    lowered = value.lower()
    lowered = re.sub(r"\.[a-z]{2}\.md$", "", lowered)
    lowered = re.sub(r"\.md$", "", lowered)
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug or "doc"


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        m = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return ""


def first_paragraph(markdown: str) -> str:
    in_code = False
    lines: List[str] = []

    for raw in markdown.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line:
            if lines:
                break
            continue
        if line.startswith("#"):
            continue
        lines.append(line)

    paragraph = " ".join(lines)
    paragraph = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", paragraph)
    paragraph = re.sub(r"`([^`]+)`", r"\1", paragraph)
    paragraph = re.sub(r"\s+", " ", paragraph).strip()
    if len(paragraph) > 180:
        paragraph = paragraph[:177].rstrip() + "..."
    return paragraph


def normalize_locale_markdown(path: pathlib.Path) -> bool:
    name = path.name.lower()
    m = re.search(r"\.([a-z]{2})\.md$", name)
    if not m:
        return True
    return m.group(1) == "en"


def match_any(path_posix: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path_posix, pattern) for pattern in patterns)


def derive_category(repo_key: str, source_rel: pathlib.Path, existing_fm: Dict[str, object]) -> str:
    existing = str(existing_fm.get("category", "")).strip()
    if existing:
        return slugify(f"{repo_key}-{existing}")

    parts = list(source_rel.parts)
    if parts and parts[0] == "docs":
        if len(parts) > 2:
            return slugify(f"{repo_key}-{parts[1]}")
        return slugify(f"{repo_key}-general")

    if parts:
        return slugify(f"{repo_key}-{parts[0]}")
    return slugify(f"{repo_key}-general")


def derive_slug(source_rel: pathlib.Path) -> str:
    rel = source_rel.as_posix()
    if rel.startswith("docs/"):
        rel = rel[5:]
    return slugify(rel.replace("/", "-"))


def normalize_order(value: object) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return 100


def normalize_last_updated(value: object) -> str:
    text = str(value or "").strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return text
    return dt.date.today().isoformat()


def build_frontmatter(
    source: SourceSpec,
    source_rel: pathlib.Path,
    existing_fm: Dict[str, object],
    body: str,
    default_version: str,
) -> Dict[str, object]:
    title = str(existing_fm.get("title", "")).strip() or first_heading(body) or source_rel.stem
    description = str(existing_fm.get("description", "")).strip() or first_paragraph(body) or f"Imported from {source.repo}."

    slug = derive_slug(source_rel)

    frontmatter: Dict[str, object] = {
        "id": str(existing_fm.get("id", "")).strip() or f"{source.repo_key}-{slug}",
        "cluster": str(existing_fm.get("cluster", "")).strip() or source.cluster,
        "category": derive_category(source.repo_key, source_rel, existing_fm),
        "order": normalize_order(existing_fm.get("order")),
        "status": str(existing_fm.get("status", "")).strip() or "active",
        "version": str(existing_fm.get("version", "")).strip() or default_version,
        "title": title,
        "description": description,
        "last_updated": normalize_last_updated(existing_fm.get("last_updated")),
        "source_locale": "en",
        "locale": "en",
        "source_repo": source.repo,
        "source_branch": source.branch,
        "source_path": source_rel.as_posix(),
        "managed_by": "sync_private_docs",
    }

    missing = REQUIRED_FRONTMATTER - set(frontmatter.keys())
    if missing:
        raise RuntimeError(f"missing required frontmatter fields: {sorted(missing)}")

    return frontmatter


def clone_repository(source: SourceSpec, token: str, clone_root: pathlib.Path) -> pathlib.Path:
    target = clone_root / source.repo_key
    if target.exists():
        shutil.rmtree(target)

    repo_url = f"https://x-access-token:{token}@github.com/{source.repo}.git"
    try:
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                source.branch,
                "--no-tags",
                repo_url,
                str(target),
            ]
        )
    except RuntimeError as exc:
        detail = str(exc).lower()
        if "authentication failed" in detail or "repository not found" in detail:
            raise RuntimeError(
                f"Unable to read private source '{source.repo}'. Verify DOCS_SYNC_GITHUB_TOKEN "
                "is a valid fine-grained or classic PAT with repository Contents: read access "
                "and that the token is authorized for this repository."
            ) from None
        raise
    return target


def resolve_local_repository(source: SourceSpec, local_root: pathlib.Path | None) -> pathlib.Path:
    if source.local_path:
        target = pathlib.Path(source.local_path).expanduser().resolve()
        if not target.exists() or not target.is_dir():
            raise RuntimeError(f"local source repo not found: {target}")
        return target

    if local_root is None:
        raise RuntimeError(
            f"local root is not configured for source '{source.repo_key}' and no local_path override is set"
        )

    repo_name = source.repo.split("/")[-1]
    target = local_root / repo_name
    if not target.exists() or not target.is_dir():
        raise RuntimeError(f"local source repo not found: {target}")
    return target


def has_accessible_local_path(source: SourceSpec) -> bool:
    if not source.local_path:
        return False
    try:
        return pathlib.Path(source.local_path).expanduser().is_dir()
    except OSError:
        return False


def relative(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> int:
    token = os.getenv("DOCS_SYNC_GITHUB_TOKEN", "").strip()
    local_root_raw = os.getenv("DOCS_SYNC_LOCAL_ROOT", "").strip()
    local_root = pathlib.Path(local_root_raw).resolve() if local_root_raw else None
    source_keys_raw = os.getenv("DOCS_SYNC_SOURCE_KEYS", "").strip()
    source_keys = {x.strip() for x in source_keys_raw.split(",") if x.strip()}

    if not token and local_root is None:
        raise RuntimeError("DOCS_SYNC_GITHUB_TOKEN is required (or use DOCS_SYNC_LOCAL_ROOT for local bootstrap)")

    default_version, sources = load_sources(SOURCES_CONFIG)
    if source_keys:
        sources = [s for s in sources if s.repo_key in source_keys]
        if not sources:
            raise RuntimeError(
                f"DOCS_SYNC_SOURCE_KEYS specified but no matching sources found: {sorted(source_keys)}"
            )
    selected_source_repos = {s.repo for s in sources}
    partial_source_sync = bool(source_keys)

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    clone_root = TMP_DIR / "source-repos"
    if local_root is None:
        if clone_root.exists():
            shutil.rmtree(clone_root)
        clone_root.mkdir(parents=True, exist_ok=True)

    generated_files: Set[pathlib.Path] = set()
    changed_files: List[pathlib.Path] = []
    skipped_non_english: List[str] = []
    skipped_sources: List[Dict[str, str]] = []
    synced_source_repos: Set[str] = set()

    for source in sources:
        try:
            if local_root is not None:
                repo_dir = resolve_local_repository(source, local_root)
            elif has_accessible_local_path(source):
                repo_dir = resolve_local_repository(source, None)
            else:
                repo_dir = clone_repository(source, token, clone_root)
        except Exception as exc:
            if source.optional:
                print(
                    f"WARN: optional source '{source.repo_key}' skipped: {exc}",
                    file=sys.stderr,
                )
                skipped_sources.append({"repo": source.repo, "reason": str(exc)})
                continue
            raise

        synced_source_repos.add(source.repo)

        for md_path in sorted(repo_dir.rglob("*.md")):
            source_rel = md_path.relative_to(repo_dir)
            source_rel_posix = source_rel.as_posix()

            if not match_any(source_rel_posix, source.include_globs):
                continue
            if source.exclude_globs and match_any(source_rel_posix, source.exclude_globs):
                continue
            if not normalize_locale_markdown(md_path):
                continue

            text = md_path.read_text(encoding="utf-8")
            existing_fm, body = parse_markdown_doc(text)

            locale_hint = str(existing_fm.get("locale", "")).strip().lower()
            if locale_hint and locale_hint != "en":
                skipped_non_english.append(f"{source.repo}:{source_rel_posix}")
                continue

            if is_probably_non_english(text):
                skipped_non_english.append(f"{source.repo}:{source_rel_posix}")
                continue

            frontmatter = build_frontmatter(
                source=source,
                source_rel=source_rel,
                existing_fm=existing_fm,
                body=body,
                default_version=default_version,
            )

            category = str(frontmatter["category"])
            slug = derive_slug(source_rel)
            target_path = CONTENT_DIR / source.cluster / category / f"{slug}.en.md"
            target_path.parent.mkdir(parents=True, exist_ok=True)

            rendered = dump_markdown_doc(frontmatter, body)
            if not target_path.exists() or target_path.read_text(encoding="utf-8") != rendered:
                target_path.write_text(rendered, encoding="utf-8")
                changed_files.append(target_path)
                print(f"synced: {relative(target_path)}")

            generated_files.add(target_path.resolve())

    removed_files: List[pathlib.Path] = []
    for path in CONTENT_DIR.rglob("*.en.md"):
        try:
            fm, _ = parse_markdown_doc(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        if str(fm.get("managed_by", "")) != "sync_private_docs":
            continue
        source_repo = str(fm.get("source_repo", "")).strip()
        if source_repo not in synced_source_repos:
            continue
        if partial_source_sync and source_repo not in selected_source_repos:
            continue
        if path.resolve() in generated_files:
            continue

        path.unlink()
        removed_files.append(path)
        print(f"removed stale: {relative(path)}")

    synced_sorted = sorted(generated_files, key=lambda p: relative(p))
    (TMP_DIR / "synced-english-files.txt").write_text(
        "\n".join(relative(p) for p in synced_sorted) + "\n",
        encoding="utf-8",
    )

    report = {
        "event": "docs.source.sync",
        "synced_english": [relative(p) for p in synced_sorted],
        "changed_english": [relative(p) for p in changed_files],
        "removed_english": [relative(p) for p in removed_files],
        "skipped_non_english": skipped_non_english,
        "sources": sorted(synced_source_repos),
        "skipped_sources": skipped_sources,
    }
    (TMP_DIR / "source-sync-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
