import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "machine_report.py"
SPEC = importlib.util.spec_from_file_location("ek_machine_report", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class MachineReportTests(unittest.TestCase):
    def test_skill_claim_does_not_upgrade_doctor_operational_status(self):
        skills = {
            "roots": [{"path": "~/.codex/skills", "exists": True, "is_dir": True}],
            "skills": [{
                "name": "candidate",
                "path": "~/.codex/skills/candidate",
                "capability_claims": [{
                    "capability": "x.search",
                    "provider": "candidate-provider",
                    "coverage_grade": "EQUIVALENT",
                    "claim_status": "DECLARED_ONLY",
                }],
            }],
        }
        doctor = {
            "runtime": "test",
            "inventory_scope": "test runtime",
            "capabilities": [{
                "id": "x.search",
                "operational_status": "UNKNOWN",
                "best_provider": None,
                "best_available_coverage": "UNKNOWN",
                "plan_action": "TARGETED_DIAGNOSIS",
            }],
        }
        receipt = mod.build_receipt(skills, doctor)
        cap = receipt["capabilities"][0]
        self.assertEqual(cap["operational_status"], "UNKNOWN")
        self.assertEqual(cap["skill_carriers"][0]["skill"], "candidate")
        self.assertEqual(receipt["interpretation"]["operational_status_source"], "Doctor report only")

    def test_unclassified_and_unmatched_claims_remain_visible(self):
        skills = {
            "skills": [
                {"name": "plain", "path": "/plain", "capability_claims": []},
                {"name": "new", "path": "/new", "capability_claims": [{
                    "capability": "new.cap",
                    "provider": "new-provider",
                    "claim_status": "DECLARED_ONLY",
                }]},
            ]
        }
        doctor = {"capabilities": []}
        receipt = mod.build_receipt(skills, doctor)
        self.assertEqual(receipt["unclassified_skills"][0]["name"], "plain")
        self.assertEqual(receipt["unmatched_capability_claims"][0]["capability"], "new.cap")

    def test_machine_report_never_marks_environment_mutation(self):
        receipt = mod.build_receipt({"skills": []}, {"capabilities": []})
        self.assertFalse(receipt["environment_mutation_attempted"])


if __name__ == "__main__":
    unittest.main()
