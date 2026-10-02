#!/usr/bin/env python3
"""
Auto-localize changed English docs using Gemini.

- Detects changed *.en.md files from git diff.
- Parses YAML frontmatter + markdown body.
- Translates title/description/body into target locales.
- Writes localized sibling files (*.uk.md, *.ru.md).
"""

from __future__ import annotations

import difflib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

import requests
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / ".tmp"
CONTENT_DIR = ROOT / "content"
LOCALES_CONFIG = ROOT / "config" / "locales.json"
GLOSSARY_CONFIG = ROOT / "scripts" / "glossary.json"

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

DEFAULT_GEMINI_MODEL_FALLBACKS = [
    "gemini-3.8-flash",
    "gemini-3.8-flash-latest",
]

TRANSIENT_HTTP_STATUSES = {429, 500, 502, 503, 504}


@dataclass
class DocParts:
    frontmatter: Dict[str, object]
    body: str


@dataclass
class GeminiModelInfo:
    name: str
    supported_methods: List[str]


def run(cmd: List[str]) -> str:
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def load_json(path: pathlib.Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_markdown_doc(path: pathlib.Path) -> DocParts:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError(f"invalid frontmatter block: {path}")

    fm_raw = parts[0][4:]
    body = parts[1]
    frontmatter = yaml.safe_load(fm_raw) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"frontmatter must be an object: {path}")

    missing = REQUIRED_FRONTMATTER - set(frontmatter.keys())
    if missing:
        raise ValueError(f"missing required frontmatter keys in {path}: {sorted(missing)}")

    return DocParts(frontmatter=frontmatter, body=body)


def dump_markdown_doc(parts: DocParts) -> str:
    fm = yaml.safe_dump(parts.frontmatter, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{fm}\n---\n{parts.body.strip()}\n"


def git_changed_english_docs(base_sha: str | None, head_sha: str | None, content_glob: str) -> List[pathlib.Path]:
    candidates: List[str] = []

    def append_from_cmd(cmd: List[str]) -> None:
        try:
            out = run(cmd)
        except Exception:
            return
        for line in out.splitlines():
            p = line.strip()
            if p:
                candidates.append(p)

    if base_sha and head_sha:
        append_from_cmd(["git", "diff", "--name-only", base_sha, head_sha, "--", content_glob])

    if not candidates:
        # Important for workflow mode: source sync step updates working tree before commit.
        append_from_cmd(["git", "diff", "--name-only", "--", content_glob])
        append_from_cmd(["git", "diff", "--name-only", "--cached", "--", content_glob])
        append_from_cmd(["git", "ls-files", "--others", "--exclude-standard", content_glob])

    if not candidates:
        append_from_cmd(["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", content_glob])

    if not candidates:
        append_from_cmd(["git", "ls-files", content_glob])

    changed: List[pathlib.Path] = []
    for p in candidates:
        if not p.endswith(".en.md"):
            continue
        abs_path = ROOT / p
        if abs_path.exists():
            changed.append(abs_path)

    seen = set()
    unique = []
    for p in changed:
        if p in seen:
            continue
        seen.add(p)
        unique.append(p)
    return unique


def list_english_docs(content_glob: str) -> List[pathlib.Path]:
    docs = [p for p in ROOT.glob(content_glob) if p.is_file() and p.name.endswith(".en.md")]
    docs.sort()
    return docs


def english_docs_missing_locales(content_glob: str, target_locales: List[str]) -> List[pathlib.Path]:
    out: List[pathlib.Path] = []
    for source in list_english_docs(content_glob):
        has_missing = False
        for locale in target_locales:
            locale_code = str(locale).strip()
            if not locale_code:
                continue
            out_path = localized_path(source, locale_code)
            if not out_path.exists():
                has_missing = True
                break
        if has_missing:
            out.append(source)
    return out


def unique_paths(paths: List[pathlib.Path]) -> List[pathlib.Path]:
    seen = set()
    out: List[pathlib.Path] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out


def _normalize_text_for_compare(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def _count_latin(text: str) -> int:
    return len(re.findall(r"[A-Za-z]", str(text or "")))


def _count_cyrillic(text: str) -> int:
    return len(re.findall(r"[А-Яа-яЁёІЇЄієїґҐ]", str(text or "")))


def is_translation_suspicious(source_text: str, translated_text: str, target_locale: str, scope: str = "body") -> bool:
    locale = str(target_locale or "").strip().lower()
    if locale not in {"ru", "uk"}:
        return False

    src = str(source_text or "")
    out = str(translated_text or "")
    src_n = _normalize_text_for_compare(src)
    out_n = _normalize_text_for_compare(out)
    if not src_n or not out_n:
        return False

    src_latin = _count_latin(src)
    out_latin = _count_latin(out)
    out_cyr = _count_cyrillic(out)

    # Strict check for short fields (title/description): identical output means no translation.
    if scope in {"title", "description"}:
        if src_latin >= 8 and out_n == src_n:
            return True
        if src_latin >= 12 and out_cyr == 0 and out_latin >= 10:
            similarity = difflib.SequenceMatcher(None, src_n[:2000], out_n[:2000]).ratio()
            if similarity >= 0.85:
                return True
        return False

    # Body check is intentionally conservative to avoid false positives on code-heavy docs.
    if src_latin >= 250 and out_cyr <= 8 and out_latin >= 150:
        similarity = difflib.SequenceMatcher(None, src_n[:20000], out_n[:20000]).ratio()
        if similarity >= 0.80:
            return True

    return False


def english_docs_with_stale_locales(content_glob: str, target_locales: List[str]) -> List[pathlib.Path]:
    stale_sources: List[pathlib.Path] = []

    for source in list_english_docs(content_glob):
        try:
            source_parts = parse_markdown_doc(source)
        except Exception:
            continue

        source_title = str(source_parts.frontmatter.get("title", ""))
        source_description = str(source_parts.frontmatter.get("description", ""))
        source_body = source_parts.body

        stale = False
        for locale in target_locales:
            locale_code = str(locale).strip()
            if not locale_code:
                continue

            locale_path = localized_path(source, locale_code)
            if not locale_path.exists():
                continue

            try:
                localized_parts = parse_markdown_doc(locale_path)
            except Exception:
                stale = True
                break

            translation_status = str(localized_parts.frontmatter.get("translation_status", "")).strip().lower()
            if translation_status == "pending":
                stale = True
                break

            localized_title = str(localized_parts.frontmatter.get("title", ""))
            localized_description = str(localized_parts.frontmatter.get("description", ""))

            if is_translation_suspicious(source_title, localized_title, locale_code, "title"):
                stale = True
                break
            if is_translation_suspicious(source_description, localized_description, locale_code, "description"):
                stale = True
                break
            if is_translation_suspicious(source_body, localized_parts.body, locale_code, "body"):
                stale = True
                break

        if stale:
            stale_sources.append(source)

    return stale_sources


def build_prompt(text: str, target_locale: str, protected_terms: List[str]) -> str:
    glossary = "\n".join(f"- {term}" for term in protected_terms)
    return (
        "You are a technical translator for software architecture documentation.\n"
        f"Target locale: {target_locale}.\n"
        "Rules:\n"
        "1) Preserve markdown formatting exactly.\n"
        "2) Do not translate protected terms.\n"
        "3) Keep code blocks, endpoint paths, and identifiers unchanged.\n"
        "4) Return only translated text, without explanations.\n\n"
        "Protected terms:\n"
        f"{glossary}\n\n"
        "Text to translate:\n"
        f"{text}"
    )


def normalize_model_name(name: str) -> str:
    name = name.strip()
    if name.startswith("models/"):
        return name.split("/", 1)[1]
    return name


def model_from_cascade_entry(entry: object) -> str:
    if isinstance(entry, str):
        return normalize_model_name(entry)

    if isinstance(entry, dict):
        for key in ("model", "model_id", "id", "code"):
            raw = str(entry.get(key, "")).strip()
            if raw:
                return normalize_model_name(raw)

    return ""


def load_configured_model_cascade(config: Dict[str, object]) -> List[str]:
    raw = config.get("gemini_model_cascade", [])
    if not isinstance(raw, list):
        return []

    out: List[str] = []
    seen = set()
    for item in raw:
        model = model_from_cascade_entry(item)
        if not model or model in seen:
            continue
        seen.add(model)
        out.append(model)
    return out


def build_model_candidates(preferred_model: str, configured_cascade: List[str] | None = None) -> List[str]:
    env_fallbacks = [
        normalize_model_name(x)
        for x in os.getenv("GEMINI_FALLBACK_MODELS", "").split(",")
        if x.strip()
    ]

    preferred_model = normalize_model_name(preferred_model)

    candidates: List[str] = []
    if configured_cascade:
        candidates.extend([normalize_model_name(x) for x in configured_cascade if normalize_model_name(x)])
        if preferred_model and preferred_model not in candidates:
            candidates.insert(0, preferred_model)
    else:
        if preferred_model.endswith("-latest"):
            candidates = [preferred_model, preferred_model[: -len("-latest")]]
        else:
            candidates = [f"{preferred_model}-latest", preferred_model]

    candidates.extend(env_fallbacks)
    candidates.extend(DEFAULT_GEMINI_MODEL_FALLBACKS)

    unique: List[str] = []
    seen = set()
    for model in candidates:
        if not model or model in seen:
            continue
        seen.add(model)
        unique.append(model)
    return unique


def fetch_available_models(api_key: str) -> List[GeminiModelInfo]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    out: List[GeminiModelInfo] = []
    for item in data.get("models", []):
        if not isinstance(item, dict):
            continue
        raw_name = str(item.get("name", "")).strip()
        name = normalize_model_name(raw_name)
        if not name:
            continue
        methods = [str(x) for x in item.get("supportedGenerationMethods", []) if str(x).strip()]
        out.append(GeminiModelInfo(name=name, supported_methods=methods))
    return out


def resolve_gemini_model(api_key: str, preferred_model: str, configured_cascade: List[str] | None = None) -> str:
    candidates = build_model_candidates(preferred_model, configured_cascade)
    try:
        available = fetch_available_models(api_key)
    except Exception as exc:
        print(
            f"WARN: unable to list Gemini models; using fallback candidate '{candidates[0]}': {exc}",
            file=sys.stderr,
        )
        return candidates[0]

    generative = [
        m.name
        for m in available
        if "generateContent" in m.supported_methods or "streamGenerateContent" in m.supported_methods
    ]
    if not generative:
        generative = [m.name for m in available]

    available_set = set(generative)
    for candidate in candidates:
        if candidate in available_set:
            return candidate

    for candidate in candidates:
        base = candidate[: -len("-latest")] if candidate.endswith("-latest") else candidate
        for available_name in generative:
            if available_name.startswith(base):
                return available_name

    for available_name in generative:
        if "flash" in available_name:
            return available_name

    if generative:
        return generative[0]

    raise RuntimeError("no Gemini models available for generateContent")


def gemini_translate(
    api_key: str,
    models: List[str],
    text: str,
    target_locale: str,
    protected_terms: List[str],
    content_scope: str = "body",
) -> Tuple[str, str]:
    if not models:
        raise RuntimeError("no Gemini models configured")

    if not text.strip():
        return text, models[0]

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": build_prompt(text=text, target_locale=target_locale, protected_terms=protected_terms)
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "topP": 0.9,
            "maxOutputTokens": 8192
        }
    }

    last_error = None
    try:
        max_retries = max(0, int(os.getenv("GEMINI_MAX_RETRIES", "3")))
    except ValueError:
        max_retries = 3
    try:
        retry_base_seconds = float(os.getenv("GEMINI_RETRY_BASE_SECONDS", "1.5"))
    except ValueError:
        retry_base_seconds = 1.5

    for idx, model in enumerate(models):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        resp = None
        for attempt in range(max_retries + 1):
            try:
                resp = requests.post(url, json=payload, timeout=120)
            except requests.RequestException as exc:
                if attempt >= max_retries:
                    raise
                delay = retry_base_seconds * (2 ** attempt)
                print(
                    f"WARN: request to Gemini model '{model}' failed ({exc}); retrying in {delay:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue

            if resp.status_code in TRANSIENT_HTTP_STATUSES and attempt < max_retries:
                delay = retry_base_seconds * (2 ** attempt)
                print(
                    f"WARN: Gemini model '{model}' returned HTTP {resp.status_code}; retrying in {delay:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue

            break

        if resp is None:
            raise RuntimeError(f"unable to get response from Gemini model '{model}'")

        if resp.status_code >= 400:
            detail = ""
            try:
                detail = str((resp.json() or {}).get("error", {}).get("message", "")).strip()
            except Exception:
                detail = resp.text.strip()

            detail_l = detail.lower()
            if resp.status_code == 429 and (
                "quota" in detail_l
                or "billing" in detail_l
                or "resource_exhausted" in detail_l
                or "rate" in detail_l
            ):
                short_detail = detail[:180] if detail else "quota/rate exhausted"
                if idx < len(models) - 1:
                    print(
                        f"WARN: Gemini model '{model}' exhausted quota/rate ({short_detail}); trying next candidate",
                        file=sys.stderr,
                    )
                    last_error = f"{model}: HTTP 429 {short_detail}"
                    continue
                raise RuntimeError(f"gemini quota/rate exhausted: {short_detail}")

            can_retry_with_next = resp.status_code in TRANSIENT_HTTP_STATUSES and idx < len(models) - 1
            if can_retry_with_next:
                short_detail = detail[:180] if detail else "temporary upstream error"
                print(
                    f"WARN: Gemini model '{model}' still failing with HTTP {resp.status_code} after retries ({short_detail}); trying next candidate",
                    file=sys.stderr,
                )
                last_error = f"{model}: HTTP {resp.status_code} {short_detail}"
                continue

            can_retry_with_next = resp.status_code in (400, 403, 404) and idx < len(models) - 1
            if can_retry_with_next:
                short_detail = detail[:180] if detail else "model unavailable"
                print(
                    f"WARN: Gemini model '{model}' failed with HTTP {resp.status_code} ({short_detail}); trying next candidate",
                    file=sys.stderr,
                )
                last_error = f"{model}: HTTP {resp.status_code} {short_detail}"
                continue

            resp.raise_for_status()

        data = resp.json()

        candidates = data.get("candidates") or []
        if not candidates:
            raise RuntimeError(f"gemini response has no candidates (model: {model})")

        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
        )
        text_out = "".join(str(p.get("text", "")) for p in parts)
        text_out = text_out.strip()
        if not text_out:
            raise RuntimeError(f"gemini response is empty (model: {model})")

        if is_translation_suspicious(text, text_out, target_locale, content_scope):
            short_detail = f"suspicious untranslated output ({target_locale}, {content_scope})"
            if idx < len(models) - 1:
                print(
                    f"WARN: Gemini model '{model}' produced {short_detail}; trying next candidate",
                    file=sys.stderr,
                )
                last_error = f"{model}: {short_detail}"
                continue
            raise RuntimeError(short_detail)

        return text_out, model

    if last_error:
        raise RuntimeError(f"all Gemini model candidates failed; last error: {last_error}")
    raise RuntimeError("all Gemini model candidates failed")


def localized_path(source_path: pathlib.Path, locale: str) -> pathlib.Path:
    return pathlib.Path(str(source_path).replace(".en.md", f".{locale}.md"))


def relative(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def cleanup_pending_locale_fallbacks(target_locales: List[str]) -> List[pathlib.Path]:
    removed: List[pathlib.Path] = []
    locale_set = {str(x).strip() for x in target_locales if str(x).strip()}
    if not locale_set:
        return removed

    for path in CONTENT_DIR.rglob("*.md"):
        name = path.name.lower()
        locale_match = re.search(r"\.([a-z]{2})\.md$", name)
        if not locale_match:
            continue
        locale = locale_match.group(1)
        if locale not in locale_set:
            continue

        try:
            parts = parse_markdown_doc(path)
        except Exception:
            continue

        translation_status = str(parts.frontmatter.get("translation_status", "")).strip().lower()
        source_locale = str(parts.frontmatter.get("source_locale", "")).strip().lower()
        if translation_status != "pending" or source_locale != "en":
            continue

        path.unlink()
        removed.append(path)
        print(f"removed pending fallback: {relative(path)}")

    return removed


def main() -> int:
    config = load_json(LOCALES_CONFIG)
    glossary = load_json(GLOSSARY_CONFIG)

    source_locale = str(config.get("source_locale", "en"))
    target_locales = list(config.get("target_locales", []))
    preferred_model = str(config.get("gemini_model", "gemini-2.5-flash"))
    configured_cascade = load_configured_model_cascade(config)
    content_glob = str(config.get("content_glob", "content/**/*.en.md"))
    allow_pending_fallback = os.getenv("TRANSLATION_ALLOW_PENDING_FALLBACK", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }

    if source_locale != "en":
        raise RuntimeError("this script currently supports en source locale only")

    protected_terms = [str(x) for x in glossary.get("protected_terms", [])]

    base_sha = os.getenv("BASE_SHA")
    head_sha = os.getenv("HEAD_SHA")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    translate_all = os.getenv("TRANSLATE_ALL", "").strip().lower() in {"1", "true", "yes"}

    if not allow_pending_fallback:
        cleanup_pending_locale_fallbacks([str(x) for x in target_locales])

    changed_en = git_changed_english_docs(base_sha, head_sha, content_glob)
    missing_locale_sources = english_docs_missing_locales(content_glob, [str(x) for x in target_locales])
    stale_locale_sources = english_docs_with_stale_locales(content_glob, [str(x) for x in target_locales])

    if translate_all:
        changed_en = list_english_docs(content_glob)
        print(f"TRANSLATE_ALL enabled: processing all English docs ({len(changed_en)} file(s)).")
    else:
        if missing_locale_sources:
            changed_en = unique_paths(changed_en + missing_locale_sources)
            print(
                f"Detected missing locale files for {len(missing_locale_sources)} English source file(s); added to translation queue."
            )
        if stale_locale_sources:
            changed_en = unique_paths(changed_en + stale_locale_sources)
            print(
                f"Detected stale locale files for {len(stale_locale_sources)} English source file(s); added to translation queue."
            )

    if not changed_en:
        print("No changed English docs detected.")
        return 0

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is required")

    model = resolve_gemini_model(api_key, preferred_model, configured_cascade)
    model_candidates = [model] + [m for m in build_model_candidates(preferred_model, configured_cascade) if m != model]
    strict_translation = os.getenv("TRANSLATION_STRICT", "").strip().lower() in {"1", "true", "yes"}

    try:
        available_models = fetch_available_models(api_key)
        available_generative = [
            m.name
            for m in available_models
            if "generateContent" in m.supported_methods or "streamGenerateContent" in m.supported_methods
        ]
        if available_generative:
            available_set = set(available_generative)
            filtered: List[str] = []
            for candidate in model_candidates:
                if candidate in available_set:
                    if candidate not in filtered:
                        filtered.append(candidate)
                    continue

                base = candidate[: -len("-latest")] if candidate.endswith("-latest") else candidate
                matched = next((m for m in available_generative if m.startswith(base)), "")
                if matched and matched not in filtered:
                    filtered.append(matched)
            if filtered:
                model_candidates = filtered
            else:
                preferred_available = [m for m in available_generative if m.startswith("gemini")]
                model_candidates = preferred_available[:5] if preferred_available else available_generative[:5]
    except Exception as exc:
        print(f"WARN: unable to filter model candidates by ListModels: {exc}", file=sys.stderr)

    print(f"Using Gemini model: {model_candidates[0]}")
    print(f"Gemini cascade order: {', '.join(model_candidates)}")

    def translate_text(text: str, locale: str, scope: str = "body") -> str:
        nonlocal model_candidates
        translated, used_model = gemini_translate(
            api_key,
            model_candidates,
            text,
            locale,
            protected_terms,
            content_scope=scope,
        )
        if used_model != model_candidates[0]:
            model_candidates = [used_model] + [m for m in model_candidates if m != used_model]
            print(f"Switched Gemini model: {used_model}")
        return translated

    TMP_DIR.mkdir(parents=True, exist_ok=True)

    localized_written: List[pathlib.Path] = []

    for source in changed_en:
        parts = parse_markdown_doc(source)

        title_en = str(parts.frontmatter.get("title", ""))
        description_en = str(parts.frontmatter.get("description", ""))
        body_en = parts.body

        for locale in target_locales:
            locale = str(locale)
            out_path = localized_path(source, locale)

            try:
                translated_title = translate_text(title_en, locale, "title")
                translated_description = translate_text(description_en, locale, "description")
                translated_body = translate_text(body_en, locale, "body")
            except Exception as exc:
                if strict_translation:
                    raise
                if out_path.exists():
                    if not allow_pending_fallback:
                        try:
                            existing = parse_markdown_doc(out_path)
                            is_pending = str(existing.frontmatter.get("translation_status", "")).strip().lower() == "pending"
                            if is_pending:
                                out_path.unlink()
                                print(
                                    f"WARN: translation failed for {relative(source)} ({locale}): {exc}; removed stale pending fallback {relative(out_path)}",
                                    file=sys.stderr,
                                )
                                continue
                        except Exception:
                            pass

                    print(
                        f"WARN: translation failed for {relative(source)} ({locale}): {exc}; keeping existing {relative(out_path)}",
                        file=sys.stderr,
                    )
                    continue

                if not allow_pending_fallback:
                    print(
                        f"WARN: translation failed for {relative(source)} ({locale}): {exc}; skipping new locale file to avoid English fallback content",
                        file=sys.stderr,
                    )
                    continue

                fallback_fm = dict(parts.frontmatter)
                fallback_fm["title"] = title_en
                fallback_fm["description"] = description_en
                fallback_fm["source_locale"] = "en"
                fallback_fm["locale"] = locale
                fallback_fm["translation_status"] = "pending"
                out_parts = DocParts(frontmatter=fallback_fm, body=body_en)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(dump_markdown_doc(out_parts), encoding="utf-8")
                localized_written.append(out_path)
                print(
                    f"WARN: translation failed for {relative(source)} ({locale}): {exc}; wrote fallback {relative(out_path)}",
                    file=sys.stderr,
                )
                continue

            localized_fm = dict(parts.frontmatter)
            localized_fm["title"] = translated_title
            localized_fm["description"] = translated_description
            localized_fm["source_locale"] = "en"
            localized_fm["locale"] = locale

            out_parts = DocParts(frontmatter=localized_fm, body=translated_body)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(dump_markdown_doc(out_parts), encoding="utf-8")
            localized_written.append(out_path)
            print(f"generated: {relative(out_path)}")

    (TMP_DIR / "localized-files.txt").write_text(
        "\n".join(relative(p) for p in localized_written) + "\n",
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
