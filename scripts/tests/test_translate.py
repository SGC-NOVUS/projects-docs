from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import export_catalog
import translate


class FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, object]):
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, object]:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"unexpected HTTP {self.status_code}")


class TranslationProgressTests(unittest.TestCase):
    def test_checkpoint_survives_reload_and_clears_after_completed_locale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = pathlib.Path(temporary_directory) / "translation-progress.json"
            progress = translate.TranslationProgress(path)
            key = progress.key("content/doc.en.md", "source-hash", "ru", "body", "body.0", "text", "glossary")
            progress.set(key, "content/doc.en.md", "ru", "Перевод")

            resumed = translate.TranslationProgress(path)
            self.assertEqual(resumed.get(key), "Перевод")

            resumed.clear_document_locale("content/doc.en.md", "ru")
            self.assertFalse(path.exists())


class GeminiCascadeTests(unittest.TestCase):
    def test_configured_cascade_places_flash_lite_last_with_confirmed_limits(self) -> None:
        config = translate.load_json(translate.LOCALES_CONFIG)
        cascade = config["gemini_model_cascade"]

        self.assertEqual(cascade[-1]["model"], "gemini-3.5-flash-lite")
        self.assertEqual(
            {key: cascade[-1][key] for key in ("rpm", "tpm", "rpd")},
            {"rpm": 15, "tpm": 250000, "rpd": 500},
        )
        self.assertEqual(
            translate.build_model_candidates(config["gemini_model"], translate.load_configured_model_cascade(config)),
            [entry["model"] for entry in cascade],
        )

    def test_model_metadata_exposes_input_and_output_token_limits(self) -> None:
        response = FakeResponse(
            200,
            {
                "models": [
                    {
                        "name": "models/gemini-flash",
                        "supportedGenerationMethods": ["generateContent"],
                        "inputTokenLimit": 1000000,
                        "outputTokenLimit": 8192,
                    }
                ]
            },
        )
        with patch.object(translate.requests, "get", return_value=response):
            models = translate.fetch_available_models("test-key")

        self.assertEqual(models[0].input_token_limit, 1000000)
        self.assertEqual(models[0].output_token_limit, 8192)

    def test_quota_response_uses_next_model_without_retrying_same_model(self) -> None:
        responses = [
            FakeResponse(429, {"error": {"message": "RESOURCE_EXHAUSTED"}}),
            FakeResponse(
                200,
                {"candidates": [{"content": {"parts": [{"text": "Настройте сервер"}]}}]},
            ),
        ]
        with patch.object(translate.requests, "post", side_effect=responses) as post:
            result, model = translate.gemini_translate(
                "test-key",
                ["model-a", "model-b"],
                "Configure the server",
                "ru",
                [],
                content_scope="title",
            )

        self.assertEqual(result, "Настройте сервер")
        self.assertEqual(model, "model-b")
        self.assertEqual(post.call_count, 2)

    def test_exhausted_cascade_reports_quota_failure(self) -> None:
        response = FakeResponse(429, {"error": {"message": "RESOURCE_EXHAUSTED"}})
        with patch.object(translate.requests, "post", return_value=response) as post:
            with self.assertRaises(translate.GeminiQuotaExhaustedError):
                translate.gemini_translate(
                    "test-key",
                    ["model-a", "model-b"],
                    "Configure the server",
                    "ru",
                    [],
                    content_scope="title",
                )

        self.assertEqual(post.call_count, 2)

    def test_quota_order_preserves_configured_fallback_priority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tracker = translate.GeminiQuotaTracker(
                pathlib.Path(temporary_directory) / "usage.json",
                {
                    "gemini-flash": {"rpm": 5, "tpm": 250000, "rpd": 20},
                    "gemini-flash-lite": {"rpm": 15, "tpm": 250000, "rpd": 500},
                },
            )

        self.assertEqual(
            tracker.model_order(["gemini-flash", "gemini-flash-lite"]),
            ["gemini-flash", "gemini-flash-lite"],
        )

    def test_daily_quota_prevents_another_generation_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tracker = translate.GeminiQuotaTracker(
                pathlib.Path(temporary_directory) / "usage.json",
                {"gemini-flash": {"rpm": 5, "tpm": 250000, "rpd": 1}},
            )
            tracker.record_attempt("gemini-flash", 20)

            with self.assertRaises(translate.GeminiQuotaUnavailableError):
                tracker.prepare_request("gemini-flash", 20)

    def test_rpm_quota_uses_next_model_instead_of_waiting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tracker = translate.GeminiQuotaTracker(
                pathlib.Path(temporary_directory) / "usage.json",
                {"gemini-flash": {"rpm": 1, "tpm": 250000, "rpd": 20}},
            )
            tracker.record_attempt("gemini-flash", 20)

            with self.assertRaisesRegex(translate.GeminiQuotaUnavailableError, "RPM quota"):
                tracker.prepare_request("gemini-flash", 20)

    def test_tpm_quota_prevents_request_that_would_exceed_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tracker = translate.GeminiQuotaTracker(
                pathlib.Path(temporary_directory) / "usage.json",
                {"gemini-flash": {"rpm": 5, "tpm": 100, "rpd": 20}},
            )
            tracker.record_attempt("gemini-flash", 80)

            with self.assertRaisesRegex(translate.GeminiQuotaUnavailableError, "TPM quota"):
                tracker.prepare_request("gemini-flash", 21)

    def test_local_quota_exhaustion_raises_resumable_cascade_pause(self) -> None:
        limits = {
            "model-a": {"rpm": 1, "tpm": 250000, "rpd": 20},
            "model-b": {"rpm": 1, "tpm": 250000, "rpd": 20},
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            tracker = translate.GeminiQuotaTracker(
                pathlib.Path(temporary_directory) / "usage.json",
                limits,
            )
            tracker.record_attempt("model-a", 20)
            tracker.record_attempt("model-b", 20)

            with patch.object(translate.requests, "post") as post:
                with self.assertRaises(translate.GeminiQuotaExhaustedError):
                    translate.gemini_translate(
                        "test-key",
                        ["model-a", "model-b"],
                        "Configure the server",
                        "ru",
                        [],
                        content_scope="title",
                        quota_tracker=tracker,
                        model_limits=limits,
                    )

            post.assert_not_called()

    def test_rate_limit_response_classifies_per_day_quota_as_daily_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tracker = translate.GeminiQuotaTracker(
                pathlib.Path(temporary_directory) / "usage.json",
                {"gemini-flash": {"rpm": 5, "tpm": 250000, "rpd": 20}},
            )
            tracker.record_rate_limit(
                "gemini-flash",
                "Quota exceeded for generate_requests_per_model_per_day",
            )

        self.assertIn("gemini-flash", tracker.daily_blocked)

    def test_long_english_fallback_is_rejected_as_translation(self) -> None:
        text = "This is a long English technical paragraph describing the system behavior. " * 5
        self.assertTrue(translate.is_translation_suspicious(text, text, "ru", "body"))
        self.assertTrue(translate.is_translation_suspicious(text, "", "ru", "body"))


class CatalogValidationTests(unittest.TestCase):
    def test_catalog_rejects_english_fallback_and_accepts_localized_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            content = root / "content"
            content.mkdir()
            source = content / "guide.en.md"
            localized = content / "guide.ru.md"
            frontmatter = (
                "---\n"
                "id: guide\n"
                "cluster: product\n"
                "category: general\n"
                "order: 1\n"
                "status: active\n"
                "version: '1'\n"
                "last_updated: '2026-10-05'\n"
            )
            source.write_text(
                frontmatter
                + "title: Configure the service\n"
                + "description: Configure the service settings.\n"
                + "---\n\n"
                + ("The service validates configuration and applies the requested settings. " * 8),
                encoding="utf-8",
            )
            localized.write_text(
                frontmatter
                + "title: Настройка службы\n"
                + "description: Настройте параметры службы.\n"
                + "source_locale: en\n"
                + "locale: ru\n"
                + "---\n\n"
                + ("Служба проверяет конфигурацию и применяет заданные параметры. " * 8),
                encoding="utf-8",
            )
            old_content_dir = export_catalog.CONTENT_DIR
            old_root = export_catalog.ROOT
            export_catalog.CONTENT_DIR = content
            export_catalog.ROOT = root
            try:
                self.assertEqual(len(export_catalog.collect_locale("ru")), 1)
                localized.write_text(
                    frontmatter
                    + "title: Настройка службы\n"
                    + "description: Настройте параметры службы.\n"
                    + "source_locale: en\n"
                    + "locale: ru\n"
                    + "---\n\n"
                    + ("The service validates configuration and applies the requested settings. " * 8),
                    encoding="utf-8",
                )
                self.assertEqual(export_catalog.collect_locale("ru"), [])
                localized.write_text(
                    frontmatter
                    + "title: Настройка службы\n"
                    + "description: Настройте параметры службы.\n"
                    + "source_locale: en\n"
                    + "locale: ru\n"
                    + "---\n\n",
                    encoding="utf-8",
                )
                self.assertEqual(export_catalog.collect_locale("ru"), [])
            finally:
                export_catalog.CONTENT_DIR = old_content_dir
                export_catalog.ROOT = old_root


if __name__ == "__main__":
    unittest.main()
