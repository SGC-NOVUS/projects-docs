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
import datetime as dt
import hashlib
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
TRANSLATION_PROGRESS_VERSION = 1
MAX_GEMINI_REQUESTS_PER_MINUTE = 15


class GeminiQuotaExhaustedError(RuntimeError):
    pass


class GeminiTranslationQualityError(RuntimeError):
    pass


@dataclass
class DocParts:
    frontmatter: Dict[str, object]
    body: str


@dataclass
class GeminiModelInfo:
    name: str
    supported_methods: List[str]
    input_token_limit: int | None = None
    output_token_limit: int | None = None


class GeminiQuotaUnavailableError(RuntimeError):
    pass


class TranslationProgress:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.entries: Dict[str, Dict[str, str]] = {}
        if not path.exists():
            return

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"unable to read translation progress file {path}: {exc}") from exc

        if not isinstance(data, dict) or data.get("version") != TRANSLATION_PROGRESS_VERSION:
            raise RuntimeError(f"unsupported translation progress format: {path}")
        entries = data.get("entries")
        if not isinstance(entries, dict):
            raise RuntimeError(f"invalid translation progress entries: {path}")
        for key, value in entries.items():
            if (
                not isinstance(key, str)
                or not isinstance(value, dict)
                or not isinstance(value.get("translation"), str)
                or not isinstance(value.get("source"), str)
                or not isinstance(value.get("locale"), str)
            ):
                raise RuntimeError(f"invalid translation progress entry in {path}")
        self.entries = entries

    @staticmethod
    def key(
        source: str,
        source_hash: str,
        locale: str,
        scope: str,
        segment: str,
        text: str,
        glossary_hash: str,
    ) -> str:
        key_data = [source, source_hash, locale, scope, segment, text, glossary_hash]
        encoded = json.dumps(key_data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def get(self, key: str) -> str | None:
        entry = self.entries.get(key)
        return str(entry["translation"]) if entry else None

    def set(self, key: str, source: str, locale: str, translation: str) -> None:
        self.entries[key] = {
            "source": source,
            "locale": locale,
            "translation": translation,
        }
        self.save()

    def clear_document_locale(self, source: str, locale: str) -> None:
        self.entries = {
            key: value
            for key, value in self.entries.items()
            if value.get("source") != source or value.get("locale") != locale
        }
        self.save()

    def save(self) -> None:
        if not self.entries:
            self.path.unlink(missing_ok=True)
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = {
            "version": TRANSLATION_PROGRESS_VERSION,
            "entries": self.entries,
        }
        temporary_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(self.path)


class GeminiQuotaTracker:
    def __init__(self, path: pathlib.Path, limits: Dict[str, Dict[str, int]]):
        self.path = path
        self.limits = limits
        self.today = dt.datetime.now(dt.timezone.utc).date().isoformat()
        self.calls: Dict[str, int] = {}
        self.blocked_until: Dict[str, float] = {}
        self.daily_blocked: set[str] = set()
        self.events: Dict[str, List[Dict[str, float]]] = {}
        self.global_events: List[float] = []
        if not path.exists():
            return

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"unable to read Gemini quota state {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise RuntimeError(f"invalid Gemini quota state: {path}")
        if data.get("date") != self.today:
            return

        calls = data.get("calls", {})
        blocked_until = data.get("blocked_until", {})
        daily_blocked = data.get("daily_blocked", [])
        events = data.get("events", {})
        if not all(isinstance(value, dict) for value in (calls, blocked_until, events)):
            raise RuntimeError(f"invalid Gemini quota state maps: {path}")
        if not isinstance(daily_blocked, list):
            raise RuntimeError(f"invalid Gemini daily quota state: {path}")

        now = time.time()
        self.calls = {str(key): int(value) for key, value in calls.items()}
        self.blocked_until = {
            str(key): float(value)
            for key, value in blocked_until.items()
            if float(value) > now
        }
        self.daily_blocked = {str(value) for value in daily_blocked}
        self.events = {
            str(key): [
                {"at": float(event["at"]), "tokens": float(event["tokens"])}
                for event in value
                if now - float(event["at"]) < 60
            ]
            for key, value in events.items()
            if isinstance(value, list)
        }
        global_events = data.get("global_events")
        if isinstance(global_events, list):
            self.global_events = [
                float(event_at)
                for event_at in global_events
                if now - float(event_at) < 60
            ]
        else:
            self.global_events = [
                event["at"]
                for model_events in self.events.values()
                for event in model_events
            ]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = {
            "date": self.today,
            "calls": self.calls,
            "blocked_until": self.blocked_until,
            "daily_blocked": sorted(self.daily_blocked),
            "events": self.events,
            "global_events": self.global_events,
        }
        temporary_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(self.path)

    def remaining_daily(self, model: str) -> int | None:
        limit = self.limits.get(model, {}).get("rpd", 0)
        return max(0, limit - self.calls.get(model, 0)) if limit > 0 else None

    def model_order(self, models: List[str]) -> List[str]:
        return list(models)

    def prepare_request(self, model: str, estimated_tokens: int) -> None:
        limits = self.limits.get(model, {})
        rpd = limits.get("rpd", 0)
        if model in self.daily_blocked or (rpd > 0 and self.calls.get(model, 0) >= rpd):
            self.daily_blocked.add(model)
            self.save()
            raise GeminiQuotaUnavailableError(f"{model} daily request quota exhausted")

        now = time.time()
        cooldown = self.blocked_until.get(model, 0)
        if cooldown > now:
            raise GeminiQuotaUnavailableError(
                f"{model} rate limited; cooldown remains {cooldown - now:.1f}s"
            )

        rpm = limits.get("rpm", 0)
        tpm = limits.get("tpm", 0)
        events = self.events.setdefault(model, [])
        events[:] = [event for event in events if now - event["at"] < 60]
        if rpm > 0 and len(events) >= rpm:
            raise GeminiQuotaUnavailableError(
                f"{model} RPM quota exhausted ({rpm} requests per minute)"
            )
        tokens_used = sum(event["tokens"] for event in events)
        if tpm > 0 and tokens_used + estimated_tokens > tpm:
            raise GeminiQuotaUnavailableError(
                f"{model} TPM quota unavailable ({tokens_used:.0f}/{tpm} tokens used; "
                f"request reserves {estimated_tokens})"
            )

        while True:
            self.global_events[:] = [
                event_at for event_at in self.global_events if now - event_at < 60
            ]
            if len(self.global_events) < MAX_GEMINI_REQUESTS_PER_MINUTE:
                return
            delay = max(0.1, self.global_events[0] + 60 - now + 0.1)
            print(
                f"Global quota pacing: waiting {delay:.1f}s "
                f"(limit={MAX_GEMINI_REQUESTS_PER_MINUTE} requests per minute)"
            )
            time.sleep(delay)
            now = time.time()

    def record_attempt(self, model: str, estimated_tokens: int) -> None:
        now = time.time()
        self.calls[model] = self.calls.get(model, 0) + 1
        self.events.setdefault(model, []).append({"at": now, "tokens": float(estimated_tokens)})
        self.global_events.append(now)
        self.save()

    def record_usage(self, model: str, actual_tokens: int) -> None:
        events = self.events.get(model, [])
        if events:
            events[-1]["tokens"] = float(max(0, actual_tokens))
            self.save()

    def record_rate_limit(self, model: str, detail: str) -> None:
        normalized = detail.lower().replace("_", " ")
        if any(
            marker in normalized
            for marker in (
                "per day",
                "per model per day",
                "per day per model",
                "daily",
                "requests/day",
                "requests per day",
                "requests per model per day",
            )
        ):
            self.daily_blocked.add(model)
        else:
            cooldown = 60
            if any(
                marker in normalized
                for marker in ("per minute", "per min", "requests/minute", "requests per minute")
            ):
                cooldown = 60
            self.blocked_until[model] = time.time() + cooldown
        self.save()


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

def _translation_prose(text: str) -> str:
    value = str(text or "")
    value = re.sub(r"```[\s\S]*?```", " ", value)
    value = re.sub(r"`[^`]*`", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"https?://\S+", " ", value)
    return value


def is_translation_suspicious(source_text: str, translated_text: str, target_locale: str, scope: str = "body") -> bool:
    locale = str(target_locale or "").strip().lower()
    if locale not in {"ru", "uk"}:
        return False

    src = str(source_text or "")
    out = str(translated_text or "")
    src_n = _normalize_text_for_compare(src)
    out_n = _normalize_text_for_compare(out)
    if not src_n:
        return False
    if not out_n:
        return True

    src_latin = _count_latin(src)
    src_cyr = _count_cyrillic(src)
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

    prose = _translation_prose(out)
    prose_letters = _count_latin(prose) + _count_cyrillic(prose)
    prose_cyrillic = _count_cyrillic(prose)
    if prose_letters >= 80 and prose_cyrillic / prose_letters < 0.25:
        return True

    source_prose = _translation_prose(src)
    source_prose_letters = _count_latin(source_prose) + _count_cyrillic(source_prose)
    if source_prose_letters >= 250 and prose_letters < int(source_prose_letters * 0.45):
        return True

    # Body check is intentionally conservative to avoid false positives on code-heavy docs.
    similarity = difflib.SequenceMatcher(None, src_n[:20000], out_n[:20000]).ratio()
    src_len = len(src_n)
    out_len = len(out_n)

    # Truncated body output usually indicates model cut-off, not a valid translation.
    if src_len >= 1200 and out_len <= int(src_len * 0.45):
        return True

    src_starts_with_heading = bool(re.match(r"^\s{0,3}#{1,6}\s+", src))
    out_starts_with_heading = bool(re.match(r"^\s{0,3}#{1,6}\s+", out))
    if src_starts_with_heading and not out_starts_with_heading:
        return True

    src_headings = len(re.findall(r"^\s{0,3}#{1,6}\s+", src, flags=re.MULTILINE))
    out_headings = len(re.findall(r"^\s{0,3}#{1,6}\s+", out, flags=re.MULTILINE))
    if src_headings >= 3 and out_headings == 0:
        return True

    if src_latin >= 250 and out_cyr <= 8 and out_latin >= 150:
        if similarity >= 0.80:
            return True

    # Handle mixed-language source docs where EN SSOT may contain some Cyrillic.
    # Keep this strict enough to avoid false positives on code-heavy translated chunks.
    if src_latin >= 1500 and similarity >= 0.98:
        if out_latin >= int(src_latin * 0.95) and out_cyr <= int(src_cyr * 1.10) + 40:
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


def english_docs_with_pending_locales(content_glob: str, target_locales: List[str]) -> List[pathlib.Path]:
    pending_sources: List[pathlib.Path] = []

    for source in list_english_docs(content_glob):
        has_pending = False
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
                continue

            translation_status = str(localized_parts.frontmatter.get("translation_status", "")).strip().lower()
            if translation_status == "pending":
                has_pending = True
                break

        if has_pending:
            pending_sources.append(source)

    return pending_sources


def split_markdown_translation_chunks(text: str, max_chars: int) -> List[str]:
    content = str(text or "")
    if max_chars <= 0 or len(content) <= max_chars:
        return [content]

    lines = content.splitlines(keepends=True)
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0
    heading_re = re.compile(r"^\s{0,3}#{1,6}\s+")

    for line in lines:
        is_heading = bool(heading_re.match(line))

        if current and is_heading and current_len >= int(max_chars * 0.5):
            chunks.append("".join(current))
            current = [line]
            current_len = len(line)
            continue

        if current and current_len + len(line) > max_chars:
            chunks.append("".join(current))
            current = [line]
            current_len = len(line)
            continue

        current.append(line)
        current_len += len(line)

    if current:
        chunks.append("".join(current))

    return chunks


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
    preferred_model = normalize_model_name(preferred_model)

    candidates: List[str] = []
    if configured_cascade:
        candidates.extend([normalize_model_name(x) for x in configured_cascade if normalize_model_name(x)])
    else:
        env_fallbacks = [
            normalize_model_name(x)
            for x in os.getenv("GEMINI_FALLBACK_MODELS", "").split(",")
            if x.strip()
        ]
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
        out.append(
            GeminiModelInfo(
                name=name,
                supported_methods=methods,
                input_token_limit=int(item["inputTokenLimit"])
                if str(item.get("inputTokenLimit", "")).isdigit()
                else None,
                output_token_limit=int(item["outputTokenLimit"])
                if str(item.get("outputTokenLimit", "")).isdigit()
                else None,
            )
        )
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
    quota_tracker: GeminiQuotaTracker | None = None,
    model_limits: Dict[str, Dict[str, int]] | None = None,
    model_context: Dict[str, GeminiModelInfo] | None = None,
) -> Tuple[str, str]:
    if not models:
        raise RuntimeError("no Gemini models configured")

    if not text.strip():
        return text, models[0]

    prompt = build_prompt(text=text, target_locale=target_locale, protected_terms=protected_terms)
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "topP": 0.9,
            "maxOutputTokens": 8192,
        }
    }

    last_error = None
    quota_limited = False
    non_quota_failure = False
    try:
        max_retries = max(0, int(os.getenv("GEMINI_MAX_RETRIES", "3")))
    except ValueError:
        max_retries = 3
    try:
        retry_base_seconds = float(os.getenv("GEMINI_RETRY_BASE_SECONDS", "1.5"))
    except ValueError:
        retry_base_seconds = 1.5

    for idx, model in enumerate(models):
        context_info = (model_context or {}).get(model)
        limits = (model_limits or {}).get(model, {})
        max_output_tokens = 8192
        if context_info and context_info.input_token_limit:
            estimated_input_tokens = len(prompt.encode("utf-8"))
            if estimated_input_tokens > context_info.input_token_limit:
                last_error = (
                    f"{model}: prompt estimate {estimated_input_tokens} exceeds "
                    f"context input limit {context_info.input_token_limit}"
                )
                print(f"WARN: {last_error}; trying a smaller/fallback request", file=sys.stderr)
                continue
        if context_info and context_info.output_token_limit:
            max_output_tokens = min(8192, context_info.output_token_limit)
        payload["generationConfig"]["maxOutputTokens"] = max_output_tokens
        estimated_tokens = len(prompt.encode("utf-8")) + max_output_tokens
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        resp = None
        model_unavailable = False
        for attempt in range(max_retries + 1):
            if quota_tracker:
                try:
                    quota_tracker.prepare_request(model, estimated_tokens)
                except GeminiQuotaUnavailableError as exc:
                    last_error = str(exc)
                    quota_limited = True
                    print(f"WARN: {exc}; trying next model", file=sys.stderr)
                    model_unavailable = True
                    break
                quota_tracker.record_attempt(model, estimated_tokens)
            try:
                resp = requests.post(url, json=payload, timeout=120)
            except requests.RequestException as exc:
                if attempt >= max_retries:
                    last_error = f"{model}: request failed after retries ({exc})"
                    non_quota_failure = True
                    break
                delay = retry_base_seconds * (2 ** attempt)
                print(
                    f"WARN: request to Gemini model '{model}' failed ({exc}); retrying in {delay:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue

            if (
                resp.status_code in TRANSIENT_HTTP_STATUSES
                and attempt < max_retries
                and resp.status_code != 429
            ):
                delay = retry_base_seconds * (2 ** attempt)
                print(
                    f"WARN: Gemini model '{model}' returned HTTP {resp.status_code}; retrying in {delay:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue

            break

        if model_unavailable:
            continue
        if resp is None:
            if last_error and last_error.startswith(f"{model}: request failed after retries"):
                print(
                    f"WARN: Gemini model '{model}' is unreachable after retries; trying next candidate",
                    file=sys.stderr,
                )
                continue
            raise RuntimeError(f"unable to get response from Gemini model '{model}'")

        if resp.status_code >= 400:
            detail = ""
            try:
                error = (resp.json() or {}).get("error", {})
                detail_parts = [str(error.get("message", "")).strip()]
                for error_detail in error.get("details", []):
                    if isinstance(error_detail, dict):
                        detail_parts.extend(
                            str(value)
                            for value in error_detail.values()
                            if isinstance(value, (str, int, float))
                        )
                detail = " ".join(part for part in detail_parts if part)
            except Exception:
                detail = resp.text.strip()

            if resp.status_code == 429:
                quota_limited = True
                short_detail = detail[:180] if detail else "quota/rate exhausted"
                if quota_tracker:
                    quota_tracker.record_rate_limit(model, detail)
                if idx < len(models) - 1:
                    print(
                        f"WARN: Gemini model '{model}' exhausted quota/rate ({short_detail}); trying next candidate",
                        file=sys.stderr,
                    )
                    last_error = f"{model}: HTTP 429 {short_detail}"
                    continue
                raise GeminiQuotaExhaustedError(f"gemini quota/rate exhausted: {short_detail}")

            can_retry_with_next = resp.status_code in TRANSIENT_HTTP_STATUSES and idx < len(models) - 1
            if can_retry_with_next:
                non_quota_failure = True
                short_detail = detail[:180] if detail else "temporary upstream error"
                print(
                    f"WARN: Gemini model '{model}' still failing with HTTP {resp.status_code} after retries ({short_detail}); trying next candidate",
                    file=sys.stderr,
                )
                last_error = f"{model}: HTTP {resp.status_code} {short_detail}"
                continue

            can_retry_with_next = resp.status_code in (400, 403, 404) and idx < len(models) - 1
            if can_retry_with_next:
                non_quota_failure = True
                short_detail = detail[:180] if detail else "model unavailable"
                print(
                    f"WARN: Gemini model '{model}' failed with HTTP {resp.status_code} ({short_detail}); trying next candidate",
                    file=sys.stderr,
                )
                last_error = f"{model}: HTTP {resp.status_code} {short_detail}"
                continue

            resp.raise_for_status()

        data = resp.json()
        usage = data.get("usageMetadata", {})
        if quota_tracker and isinstance(usage, dict):
            actual_tokens = usage.get("totalTokenCount")
            if isinstance(actual_tokens, int):
                quota_tracker.record_usage(model, actual_tokens)

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
            raise GeminiTranslationQualityError(short_detail)

        return text_out, model

    if quota_limited and not non_quota_failure:
        raise GeminiQuotaExhaustedError(f"all Gemini model candidates exhausted: {last_error}")
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
    try:
        max_docs_per_run = max(0, int(os.getenv("TRANSLATION_MAX_DOCS_PER_RUN", "0")))
    except ValueError:
        max_docs_per_run = 0
    try:
        body_chunk_chars = max(800, int(os.getenv("TRANSLATION_BODY_CHUNK_CHARS", "1800")))
    except ValueError:
        body_chunk_chars = 1800

    if not allow_pending_fallback:
        if api_key:
            cleanup_pending_locale_fallbacks([str(x) for x in target_locales])
        else:
            print(
                "WARN: GEMINI_API_KEY is missing; skipping pending fallback cleanup to avoid deleting locale files in dry-runs.",
                file=sys.stderr,
            )

    changed_en = git_changed_english_docs(base_sha, head_sha, content_glob)
    pending_locale_sources = english_docs_with_pending_locales(content_glob, [str(x) for x in target_locales])
    missing_locale_sources = english_docs_missing_locales(content_glob, [str(x) for x in target_locales])
    stale_locale_sources = english_docs_with_stale_locales(content_glob, [str(x) for x in target_locales])

    if translate_all:
        changed_en = list_english_docs(content_glob)
        print(f"TRANSLATE_ALL enabled: processing all English docs ({len(changed_en)} file(s)).")
    else:
        if pending_locale_sources:
            changed_en = unique_paths(pending_locale_sources + changed_en)
            print(
                f"Detected pending locale files for {len(pending_locale_sources)} English source file(s); prioritized in translation queue."
            )
        if stale_locale_sources:
            changed_en = unique_paths(changed_en + stale_locale_sources)
            print(
                f"Detected stale locale files for {len(stale_locale_sources)} English source file(s); prioritized before missing locale files."
            )
        if missing_locale_sources:
            changed_en = unique_paths(changed_en + missing_locale_sources)
            print(
                f"Detected missing locale files for {len(missing_locale_sources)} English source file(s); added to translation queue."
            )

    if max_docs_per_run > 0 and len(changed_en) > max_docs_per_run:
        print(
            f"TRANSLATION_MAX_DOCS_PER_RUN={max_docs_per_run}: limiting translation queue from {len(changed_en)} to {max_docs_per_run} file(s)."
        )
        changed_en = changed_en[:max_docs_per_run]

    if not changed_en:
        print("No changed English docs detected.")
        return 0

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is required")

    model = resolve_gemini_model(api_key, preferred_model, configured_cascade)
    model_candidates = [model] + [m for m in build_model_candidates(preferred_model, configured_cascade) if m != model]
    strict_translation = os.getenv("TRANSLATION_STRICT", "").strip().lower() in {"1", "true", "yes"}

    available_models: List[GeminiModelInfo] = []
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
                raise RuntimeError(
                    "none of the configured Gemini models are available for generateContent; "
                    "refusing to use an unconfigured model without quota limits"
                )
    except Exception as exc:
        print(f"WARN: unable to filter model candidates by ListModels: {exc}", file=sys.stderr)

    print(f"Using Gemini model: {model_candidates[0]}")
    model_limits: Dict[str, Dict[str, int]] = {}
    for entry in configured_cascade:
        if isinstance(entry, dict):
            model_name = model_from_cascade_entry(entry)
            model_limits[model_name] = {
                key: int(entry[key])
                for key in ("rpm", "tpm", "rpd")
                if str(entry.get(key, "")).isdigit() and int(entry[key]) > 0
            }

    model_context: Dict[str, GeminiModelInfo] = {}
    for candidate in model_candidates:
        candidate_base = candidate.removesuffix("-latest")
        for available_model in available_models:
            available_base = available_model.name.removesuffix("-latest")
            if candidate == available_model.name or candidate_base == available_base:
                model_context[candidate] = available_model
                if candidate not in model_limits:
                    for configured_name, configured_quota in model_limits.items():
                        if configured_name.removesuffix("-latest") == candidate_base:
                            model_limits[candidate] = configured_quota
                            break
                break

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    quota_tracker = GeminiQuotaTracker(TMP_DIR / "gemini-usage.json", model_limits)
    model_candidates = quota_tracker.model_order(model_candidates)
    print(f"Gemini cascade order (configured priority): {', '.join(model_candidates)}")

    def translate_text(text: str, locale: str, scope: str = "body") -> str:
        nonlocal model_candidates
        translated, used_model = gemini_translate(
            api_key,
            model_candidates,
            text,
            locale,
            protected_terms,
            content_scope=scope,
            quota_tracker=quota_tracker,
            model_limits=model_limits,
            model_context=model_context,
        )
        if used_model != model_candidates[0]:
            print(f"Switched Gemini model: {used_model}")
        return translated

    progress = TranslationProgress(TMP_DIR / "translation-progress.json")
    glossary_hash = hashlib.sha256(
        json.dumps(protected_terms, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    localized_written: List[pathlib.Path] = []

    for source in changed_en:
        parts = parse_markdown_doc(source)
        source_name = relative(source)
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()

        title_en = str(parts.frontmatter.get("title", ""))
        description_en = str(parts.frontmatter.get("description", ""))
        body_en = parts.body

        for locale in target_locales:
            locale = str(locale)
            out_path = localized_path(source, locale)

            def translate_cached(text: str, scope: str, segment: str) -> str:
                key = progress.key(
                    source_name,
                    source_hash,
                    locale,
                    scope,
                    segment,
                    text,
                    glossary_hash,
                )
                cached = progress.get(key)
                if cached is not None:
                    print(f"resumed {scope} translation: {source_name} ({locale}, {segment})")
                    return cached

                translated = translate_text(text, locale, scope)
                progress.set(key, source_name, locale, translated)
                return translated

            try:
                translated_title = translate_cached(title_en, "title", "title")
                translated_description = translate_cached(description_en, "description", "description")

                def translate_body(text: str, target_locale: str) -> str:
                    def translate_chunk(
                        chunk_text: str,
                        chunk_chars: int,
                        segment: str,
                        depth: int = 0,
                    ) -> str:
                        key = progress.key(
                            source_name,
                            source_hash,
                            target_locale,
                            "body",
                            segment,
                            chunk_text,
                            glossary_hash,
                        )
                        cached = progress.get(key)
                        if cached is not None:
                            print(
                                f"resumed body translation: {source_name} "
                                f"({target_locale}, {segment})"
                            )
                            return cached

                        try:
                            translated = translate_text(chunk_text, target_locale, "body")
                        except GeminiQuotaExhaustedError:
                            raise
                        except Exception as exc:
                            if depth >= 3 or len(chunk_text) < 600:
                                raise

                            next_chars = max(1000, min(chunk_chars // 2, len(chunk_text) // 2))
                            subchunks = split_markdown_translation_chunks(chunk_text, next_chars)
                            if len(subchunks) <= 1:
                                raise

                            print(
                                f"WARN: body chunk translation failed for locale {target_locale} "
                                f"({exc}); retrying with smaller chunks "
                                f"({len(subchunks)} chunk(s), depth={depth + 1})",
                                file=sys.stderr,
                            )
                            translated_subchunks = [
                                translate_chunk(
                                    subchunk,
                                    next_chars,
                                    f"{segment}.{idx}",
                                    depth + 1,
                                ).strip("\n")
                                for idx, subchunk in enumerate(subchunks)
                            ]
                            translated = "\n\n".join(translated_subchunks).strip()

                        progress.set(key, source_name, target_locale, translated)
                        return translated

                    chunks = split_markdown_translation_chunks(text, body_chunk_chars)
                    translated_chunks = [
                        translate_chunk(chunk, body_chunk_chars, f"body.{idx}").strip("\n")
                        for idx, chunk in enumerate(chunks)
                    ]
                    if len(chunks) > 1:
                        print(f"Translated body chunks ({len(chunks)}) for locale {target_locale}")
                    return "\n\n".join(translated_chunks).strip()

                translated_body = translate_body(body_en, locale)
            except (GeminiQuotaExhaustedError, GeminiTranslationQualityError) as exc:
                reason = (
                    "quality validation failed"
                    if isinstance(exc, GeminiTranslationQualityError)
                    else "quota/rate limit exhausted"
                )
                print(
                    f"WARN: pausing localization at {source_name} ({locale}): {reason}: {exc}. "
                    "Completed chunks are checkpointed for the next run.",
                    file=sys.stderr,
                )
                (TMP_DIR / "localized-files.txt").write_text(
                    "\n".join(relative(path) for path in localized_written) + "\n",
                    encoding="utf-8",
                )
                return 0
            except Exception as exc:
                if strict_translation:
                    raise
                if out_path.exists():
                    if not allow_pending_fallback:
                        try:
                            existing = parse_markdown_doc(out_path)
                            is_pending = str(existing.frontmatter.get("translation_status", "")).strip().lower() == "pending"
                            existing_title = str(existing.frontmatter.get("title", ""))
                            existing_description = str(existing.frontmatter.get("description", ""))
                            is_stale = (
                                is_translation_suspicious(title_en, existing_title, locale, "title")
                                or is_translation_suspicious(description_en, existing_description, locale, "description")
                                or is_translation_suspicious(body_en, existing.body, locale, "body")
                            )
                            if is_pending:
                                out_path.unlink()
                                print(
                                    f"WARN: translation failed for {relative(source)} ({locale}): {exc}; removed pending fallback locale file {relative(out_path)}",
                                    file=sys.stderr,
                                )
                                continue
                            if is_stale:
                                out_path.unlink()
                                print(
                                    f"WARN: translation failed for {relative(source)} ({locale}): {exc}; removed stale locale file for retry {relative(out_path)}",
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
            progress.clear_document_locale(source_name, locale)
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
