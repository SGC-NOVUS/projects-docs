#!/usr/bin/env python3
"""
Smoke-check Gemini model cascade for projects-docs.

By default prints configured cascade order and metadata.
Use --probe to test cascade failover with a tiny generation request.
Use --probe-all to test every model in the cascade.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
from typing import Dict, List, Tuple

import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCALES_CONFIG = ROOT / "config" / "locales.json"
TRANSIENT_HTTP_STATUSES = {429, 500, 502, 503, 504}


def load_json(path: pathlib.Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_model_name(name: str) -> str:
    raw = str(name or "").strip()
    if raw.startswith("models/"):
        return raw.split("/", 1)[1]
    return raw


def model_from_entry(entry: object) -> str:
    if isinstance(entry, str):
        return normalize_model_name(entry)

    if isinstance(entry, dict):
        for key in ("model", "model_id", "id", "code"):
            candidate = normalize_model_name(str(entry.get(key, "")))
            if candidate:
                return candidate

    return ""


def load_cascade(config: Dict[str, object]) -> List[Dict[str, object]]:
    raw = config.get("gemini_model_cascade", [])
    out: List[Dict[str, object]] = []
    seen = set()

    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                model = model_from_entry(item)
                if not model or model in seen:
                    continue
                seen.add(model)
                out.append(
                    {
                        "name": str(item.get("name", model)).strip() or model,
                        "model": model,
                        "rpm": item.get("rpm"),
                        "tpm": item.get("tpm"),
                        "rpd": item.get("rpd"),
                        "docs_url": item.get("docs_url", ""),
                    }
                )
            elif isinstance(item, str):
                model = model_from_entry(item)
                if not model or model in seen:
                    continue
                seen.add(model)
                out.append({"name": model, "model": model, "rpm": None, "tpm": None, "rpd": None, "docs_url": ""})

    if not out:
        fallback = normalize_model_name(str(config.get("gemini_model", "gemini-3.8-flash")))
        if fallback:
            out.append({"name": fallback, "model": fallback, "rpm": None, "tpm": None, "rpd": None, "docs_url": ""})

    return out


def describe_entry(entry: Dict[str, object], idx: int) -> str:
    rpm = entry.get("rpm")
    tpm = entry.get("tpm")
    rpd = entry.get("rpd")
    docs_url = str(entry.get("docs_url", "")).strip()
    limits = f"RPM={rpm} TPM={tpm} RPD={rpd}" if any(x is not None for x in (rpm, tpm, rpd)) else "limits=n/a"
    tail = f" docs={docs_url}" if docs_url else ""
    return f"{idx}. {entry['name']} ({entry['model']}) {limits}{tail}"


def probe_model(api_key: str, model: str, timeout: int, retries: int) -> Tuple[bool, str]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": "Return only: OK"}]}],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 8,
        },
    }

    last_detail = ""
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout)
        except requests.RequestException as exc:
            last_detail = f"network error: {exc}"
            if attempt >= retries:
                return False, last_detail
            time.sleep(2**attempt)
            continue

        if resp.status_code >= 400:
            detail = ""
            try:
                detail = str((resp.json() or {}).get("error", {}).get("message", "")).strip()
            except Exception:
                detail = resp.text.strip()
            detail = detail[:220] if detail else f"HTTP {resp.status_code}"
            last_detail = f"HTTP {resp.status_code}: {detail}"

            if resp.status_code in TRANSIENT_HTTP_STATUSES and attempt < retries:
                time.sleep(2**attempt)
                continue
            return False, last_detail

        data = resp.json() if resp.content else {}
        candidates = data.get("candidates") or []
        if not candidates:
            return False, "empty candidates"

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(str(p.get("text", "")) for p in parts).strip()
        return True, text[:80] if text else "ok"

    return False, last_detail or "unknown error"


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-check Gemini cascade for projects-docs")
    parser.add_argument("--probe", action="store_true", help="Probe cascade until first successful model")
    parser.add_argument("--probe-all", action="store_true", help="Probe all models in cascade")
    parser.add_argument("--timeout", type=int, default=45, help="HTTP timeout seconds")
    parser.add_argument("--retries", type=int, default=1, help="Retries per model for transient failures")
    args = parser.parse_args()

    config = load_json(LOCALES_CONFIG)
    cascade = load_cascade(config)

    print("Gemini cascade from config/locales.json:")
    for idx, entry in enumerate(cascade, start=1):
        print(describe_entry(entry, idx))

    do_probe = args.probe or args.probe_all
    if not do_probe:
        print("Dry run complete (no network probe). Use --probe or --probe-all to test API calls.")
        return 0

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: GEMINI_API_KEY is required for --probe/--probe-all", file=sys.stderr)
        return 2

    print("Running Gemini probe without printing secrets...")

    successes = 0
    for entry in cascade:
        ok, detail = probe_model(api_key, str(entry["model"]), timeout=args.timeout, retries=max(0, args.retries))
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {entry['model']} -> {detail}")

        if ok:
            successes += 1
            if args.probe and not args.probe_all:
                print(f"Cascade probe selected model: {entry['model']}")
                return 0

    if successes > 0:
        print(f"Probe finished: {successes}/{len(cascade)} model(s) succeeded")
        return 0

    print("ERROR: all Gemini models in cascade failed probe", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
