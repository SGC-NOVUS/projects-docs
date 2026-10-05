from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import sync_private_docs


class CloneRepositoryTests(unittest.TestCase):
    def test_access_check_confirms_repository_access(self) -> None:
        response = unittest.mock.MagicMock()
        response.__enter__.return_value.status = 200
        with patch.object(sync_private_docs.urllib.request, "urlopen", return_value=response):
            sync_private_docs.verify_github_repository_access(
                "SGC-NOVUS/panel-core",
                "test-token",
            )

    def test_access_check_reports_invalid_token_without_exposing_it(self) -> None:
        token = "test-token-do-not-log"
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/SGC-NOVUS/panel-core",
            401,
            "Unauthorized",
            {},
            None,
        )
        with patch.object(sync_private_docs.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(RuntimeError) as raised:
                sync_private_docs.verify_github_repository_access(
                    "SGC-NOVUS/panel-core",
                    token,
                )

        self.assertIn("HTTP 401", str(raised.exception))
        self.assertNotIn(token, str(raised.exception))

    def test_access_check_reports_missing_private_repo_access(self) -> None:
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/SGC-NOVUS/panel-core",
            404,
            "Not Found",
            {},
            None,
        )
        with patch.object(sync_private_docs.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(RuntimeError) as raised:
                sync_private_docs.verify_github_repository_access(
                    "SGC-NOVUS/panel-core",
                    "test-token",
                )

        self.assertIn("HTTP 404", str(raised.exception))
        self.assertIn("Contents: read", str(raised.exception))

    def test_authentication_error_gives_secret_scope_guidance_without_token(self) -> None:
        source = sync_private_docs.SourceSpec(
            repo="SGC-NOVUS/panel-core",
            branch="main",
            repo_key="panel-core",
            cluster="novus-os",
            include_globs=[],
            exclude_globs=[],
            local_path="",
            optional=False,
        )
        token = "test-token-do-not-log"
        with tempfile.TemporaryDirectory() as temporary_directory:
            with patch.object(
                sync_private_docs,
                "run",
                side_effect=RuntimeError(f"Authentication failed for token {token}"),
            ):
                with self.assertRaises(RuntimeError) as raised:
                    sync_private_docs.clone_repository(
                        source,
                        token,
                        pathlib.Path(temporary_directory),
                    )

        message = str(raised.exception)
        self.assertIn("DOCS_SYNC_GITHUB_TOKEN", message)
        self.assertIn("Contents: read", message)
        self.assertNotIn(token, message)

    def test_non_authentication_clone_error_is_preserved(self) -> None:
        source = sync_private_docs.SourceSpec(
            repo="SGC-NOVUS/panel-core",
            branch="main",
            repo_key="panel-core",
            cluster="novus-os",
            include_globs=[],
            exclude_globs=[],
            local_path="",
            optional=False,
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            with patch.object(sync_private_docs, "run", side_effect=RuntimeError("network timeout")):
                with self.assertRaisesRegex(RuntimeError, "network timeout"):
                    sync_private_docs.clone_repository(
                        source,
                        "token",
                        pathlib.Path(temporary_directory),
                    )


if __name__ == "__main__":
    unittest.main()
