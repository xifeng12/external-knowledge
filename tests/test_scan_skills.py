import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "scan_skills.py"
SPEC = importlib.util.spec_from_file_location("ek_scan_skills", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class SkillInventoryTests(unittest.TestCase):
    def test_discovers_skill_without_inventing_capability(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "plain-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: plain-skill\ndescription: ordinary skill\n---\n",
                encoding="utf-8",
            )
            report = mod.scan_roots([str(root)])
            self.assertEqual(report["summary"]["skill_count"], 1)
            item = report["skills"][0]
            self.assertEqual(item["name"], "plain-skill")
            self.assertEqual(item["carrier_status"], "DISCOVERED")
            self.assertEqual(item["capability_attribution"], "UNCLASSIFIED")
            self.assertEqual(item["capability_claims"], [])

    def test_reads_only_explicit_capability_sidecar_claims(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "wechat-search"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: wechat-search\n---\n", encoding="utf-8")
            (skill / "external-knowledge.json").write_text(
                json.dumps({
                    "schema_version": 1,
                    "capability_claims": [{
                        "capability": "wechat.discovery",
                        "provider": "wechat-article-search",
                        "coverage_grade": "EQUIVALENT",
                    }],
                }),
                encoding="utf-8",
            )
            report = mod.scan_roots([str(root)])
            item = report["skills"][0]
            self.assertEqual(item["capability_attribution"], "EXPLICIT_DECLARATION")
            self.assertEqual(item["capability_claims"][0]["capability"], "wechat.discovery")
            self.assertEqual(item["capability_claims"][0]["claim_status"], "DECLARED_ONLY")

    def test_broken_sidecar_does_not_abort_scan(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "broken"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: broken\n---\n", encoding="utf-8")
            (skill / "external-knowledge.json").write_text("{not json", encoding="utf-8")
            report = mod.scan_roots([str(root)])
            self.assertEqual(report["summary"]["skill_count"], 1)
            self.assertTrue(report["skills"][0]["sidecar"]["error"])
            self.assertEqual(report["skills"][0]["capability_claims"], [])

    def test_missing_root_is_reported_not_treated_as_machine_wide_absence(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "missing"
            report = mod.scan_roots([str(missing)])
            self.assertEqual(report["summary"]["skill_count"], 0)
            self.assertFalse(report["roots"][0]["exists"])
            self.assertEqual(
                report["interpretation"]["skill_presence_proves"],
                "carrier/discovery presence only",
            )

    def test_scanner_never_marks_environment_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            report = mod.scan_roots([td])
            self.assertFalse(report["environment_mutation_attempted"])


if __name__ == "__main__":
    unittest.main()
