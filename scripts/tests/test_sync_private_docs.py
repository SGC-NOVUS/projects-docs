from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import sync_private_docs


class CloneRepositoryTests(unittest.TestCase):
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
