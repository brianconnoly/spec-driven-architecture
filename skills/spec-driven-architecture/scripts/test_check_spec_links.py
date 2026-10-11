#!/usr/bin/env python3
"""Failure and starter checks for the spec link checker."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_spec_links import check

SKILL_ROOT = Path(__file__).resolve().parents[1]
CANONICAL = SKILL_ROOT / "scripts" / "check_spec_links.py"
STARTER = SKILL_ROOT / "assets" / "starter"
STARTER_COPY = STARTER / "scripts" / "check_spec_links.py"


class CheckerTest(unittest.TestCase):
    def test_starter_copy_matches_canonical_script(self) -> None:
        self.assertEqual(CANONICAL.read_bytes(), STARTER_COPY.read_bytes())

    def test_starter_links_are_complete(self) -> None:
        self.assertEqual(check(STARTER), [])

    def test_missing_link_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "specs" / "workspace.c4").write_text(
                "model {\n  link ./missing.c4\n}\n",
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("missing link target" in error for error in errors), errors)

    def test_orphan_service_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specs = root / "specs"
            specs.mkdir()
            (specs / "workspace.c4").write_text("model {}\n", encoding="utf-8")
            (specs / "api.tsp").write_text('@service(#{ title: "Orphan" })\n', encoding="utf-8")
            errors = check(root)
            self.assertTrue(any("no LikeC4 link" in error for error in errors), errors)

    def test_linked_source_without_marker_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "src").mkdir()
            (root / "src" / "api.ts").write_text("export const name = 'api';\n", encoding="utf-8")
            (root / "specs" / "model.c4").write_text(
                "model {\n"
                "  api = component 'API' 'Owns the route.' {\n"
                "    link ../src/api.ts\n"
                "  }\n"
                "}\n",
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("no Architecture marker" in error for error in errors), errors)

    def test_wrong_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "src").mkdir()
            (root / "specs" / "model.c4").write_text(
                "model {\n  api = component 'API' 'Owns the route.' {}\n}\n",
                encoding="utf-8",
            )
            (root / "src" / "api.ts").write_text(
                "// Architecture: specs/model.c4 -> missing.api\n",
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("missing declarations" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
