#!/usr/bin/env python3
"""
Auto-localize changed English docs using Gemini.

- Detects changed *.en.md files from git diff.
- Parses YAML frontmatter + markdown body.
- Translates title/description/body into target locales.
- Writes localized sibling files (*.uk.md, *.ru.md).
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

import requests
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / ".tmp"
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
    "gemini-2.5-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
]


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


def build_model_candidates(preferred_model: str) -> List[str]:
    env_fallbacks = [
        normalize_model_name(x)
        for x in os.getenv("GEMINI_FALLBACK_MODELS", "").split(",")
        if x.strip()
    ]

    preferred_model = normalize_model_name(preferred_model)
    candidates = [preferred_model]
    if preferred_model.endswith("-latest"):
        candidates.append(preferred_model[: -len("-latest")])
    else:
        candidates.append(f"{preferred_model}-latest")

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


def resolve_gemini_model(api_key: str, preferred_model: str) -> str:
    candidates = build_model_candidates(preferred_model)
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


def gemini_translate(api_key: str, model: str, text: str, target_locale: str, protected_terms: List[str]) -> str:
    if not text.strip():
        return text

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
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

    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    candidates = data.get("candidates") or []
    if not candidates:
        raise RuntimeError("gemini response has no candidates")

    parts = (
        candidates[0]
        .get("content", {})
        .get("parts", [])
    )
    text_out = "".join(str(p.get("text", "")) for p in parts)
    text_out = text_out.strip()
    if not text_out:
        raise RuntimeError("gemini response is empty")
    return text_out


def localized_path(source_path: pathlib.Path, locale: str) -> pathlib.Path:
    return pathlib.Path(str(source_path).replace(".en.md", f".{locale}.md"))


def relative(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> int:
    config = load_json(LOCALES_CONFIG)
    glossary = load_json(GLOSSARY_CONFIG)

    source_locale = str(config.get("source_locale", "en"))
    target_locales = list(config.get("target_locales", []))
    preferred_model = str(config.get("gemini_model", "gemini-2.5-flash"))
    content_glob = str(config.get("content_glob", "content/**/*.en.md"))

    if source_locale != "en":
        raise RuntimeError("this script currently supports en source locale only")

    protected_terms = [str(x) for x in glossary.get("protected_terms", [])]

    base_sha = os.getenv("BASE_SHA")
    head_sha = os.getenv("HEAD_SHA")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    changed_en = git_changed_english_docs(base_sha, head_sha, content_glob)
    if not changed_en:
        print("No changed English docs detected.")
        return 0

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is required")

    model = resolve_gemini_model(api_key, preferred_model)
    print(f"Using Gemini model: {model}")

    TMP_DIR.mkdir(parents=True, exist_ok=True)

    localized_written: List[pathlib.Path] = []

    for source in changed_en:
        parts = parse_markdown_doc(source)

        title_en = str(parts.frontmatter.get("title", ""))
        description_en = str(parts.frontmatter.get("description", ""))
        body_en = parts.body

        for locale in target_locales:
            locale = str(locale)
            translated_title = gemini_translate(api_key, model, title_en, locale, protected_terms)
            translated_description = gemini_translate(api_key, model, description_en, locale, protected_terms)
            translated_body = gemini_translate(api_key, model, body_en, locale, protected_terms)

            localized_fm = dict(parts.frontmatter)
            localized_fm["title"] = translated_title
            localized_fm["description"] = translated_description
            localized_fm["source_locale"] = "en"
            localized_fm["locale"] = locale

            out_parts = DocParts(frontmatter=localized_fm, body=translated_body)
            out_path = localized_path(source, locale)
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
