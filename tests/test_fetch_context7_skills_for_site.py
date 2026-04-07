from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts import fetch_context7_skills_for_site as ranked


class KeepStaleSnapshotTests(unittest.TestCase):
    def test_main_keeps_existing_snapshot_when_fetch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            out_json = root / "skills-ranked.json"
            out_csv = root / "skills-ranked.csv"
            old_json = {"generatedAtUtc": "2026-04-01T00:00:00+00:00", "items": []}
            old_csv = "rank,name\n1,existing\n"
            out_json.write_text(json.dumps(old_json), encoding="utf-8")
            out_csv.write_text(old_csv, encoding="utf-8")

            argv = [
                "fetch_context7_skills_for_site.py",
                "--output-json",
                str(out_json),
                "--output-csv",
                str(out_csv),
                "--keep-stale-on-error",
            ]
            with patch.object(sys, "argv", argv):
                with patch.object(ranked, "fetch_json", side_effect=RuntimeError("HTTP 429")):
                    rc = ranked.main()

            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(out_json.read_text(encoding="utf-8")), old_json)
            self.assertEqual(out_csv.read_text(encoding="utf-8"), old_csv)


if __name__ == "__main__":
    unittest.main()
