import importlib.util
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ek_plan", ROOT / "scripts" / "plan.py")
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def doctor_report(cap_action="INSTALL_CANDIDATE", providers=None):
    return {
        "runtime": "zcode",
        "capabilities": [{
            "id": "x",
            "plan_action": cap_action,
            "providers": providers or [{
                "id": "p",
                "operational_status": "MISSING_CONFIRMED",
                "coverage_grade": "EQUIVALENT",
            }]
        }]
    }


def recipe(step=None):
    return {
        "source": "validated-test-contract",
        "steps": [step or {
            "kind": "run_command",
            "description": "install provider p",
            "argv": ["pkg", "install", "p"],
        }],
        "verification": [{
            "kind": "doctor_then_representative_probe",
            "success": "provider becomes runtime-callable",
        }],
    }


def adapter(providers=None):
    return {
        "adapter_id": "test",
        "capabilities": [{
            "id": "x",
            "providers": providers or [{
                "id": "p",
                "provisioning": {"install": recipe()},
            }]
        }]
    }


class PlannerBetaTests(unittest.TestCase):
    def test_install_candidate_with_one_valid_provider_creates_approval_plan(self):
        p = mod.build_plan(doctor_report(), adapter())
        self.assertEqual(len(p["changes"]), 1)
        self.assertTrue(p["approval_required"])
        self.assertTrue(p["plan_id"].startswith("ekp-"))
        self.assertFalse(p["environment_mutation_attempted"])

    def test_unknown_provider_cannot_become_install_plan(self):
        d = doctor_report(providers=[{
            "id": "p",
            "operational_status": "UNKNOWN",
            "coverage_grade": "EQUIVALENT",
        }])
        p = mod.build_plan(d, adapter())
        self.assertEqual(p["changes"], [])
        self.assertTrue(p["unresolved"])

    def test_missing_recipe_is_unresolved_not_improvised(self):
        a = adapter(providers=[{"id": "p"}])
        p = mod.build_plan(doctor_report(), a)
        self.assertEqual(p["changes"], [])
        self.assertIn("no provider has a validated provisioning contract", p["unresolved"][0]["reason"])

    def test_multiple_candidates_require_explicit_provider_selection(self):
        d = doctor_report(providers=[
            {"id": "a", "operational_status": "MISSING_CONFIRMED", "coverage_grade": "EQUIVALENT"},
            {"id": "b", "operational_status": "MISSING_CONFIRMED", "coverage_grade": "EQUIVALENT"},
        ])
        a = adapter(providers=[
            {"id": "a", "provisioning": {"install": recipe()}},
            {"id": "b", "provisioning": {"install": recipe()}},
        ])
        p = mod.build_plan(d, a)
        self.assertEqual(p["changes"], [])
        self.assertEqual(sorted(p["unresolved"][0]["eligible_candidates"]), ["a", "b"])

        p2 = mod.build_plan(d, a, provider_selections={"x": "b"})
        self.assertEqual(p2["changes"][0]["provider"], "b")

    def test_plan_id_changes_when_command_changes(self):
        p1 = mod.build_plan(doctor_report(), adapter())
        a2 = adapter()
        a2["capabilities"][0]["providers"][0]["provisioning"]["install"]["steps"][0]["argv"] = [
            "pkg", "install", "p", "--different"
        ]
        p2 = mod.build_plan(doctor_report(), a2)
        self.assertNotEqual(p1["plan_id"], p2["plan_id"])

    def test_plan_id_ignores_generated_at_only(self):
        p1 = mod.build_plan(doctor_report(), adapter())
        p2 = deepcopy(p1)
        p2["generated_at"] = "2099-01-01T00:00:00Z"
        self.assertEqual(mod.compute_plan_id(p1), mod.compute_plan_id(p2))

    def test_not_needed_or_keep_is_not_mutation_eligible(self):
        d = doctor_report(cap_action="DO_NOT_INSTALL")
        p = mod.build_plan(d, adapter(), requested_capabilities=["x"])
        self.assertEqual(p["changes"], [])
        self.assertIn("not eligible for mutation", p["unresolved"][0]["reason"])

    def test_run_command_shell_true_is_rejected(self):
        bad = recipe({
            "kind": "run_command",
            "description": "bad",
            "argv": ["pkg", "install", "p"],
            "shell": True,
        })
        a = adapter(providers=[{"id": "p", "provisioning": {"install": bad}}])
        p = mod.build_plan(doctor_report(), a)
        self.assertEqual(p["changes"], [])
        self.assertTrue(p["unresolved"])

    def test_verification_is_required_or_defaulted(self):
        a = adapter()
        del a["capabilities"][0]["providers"][0]["provisioning"]["install"]["verification"]
        p = mod.build_plan(doctor_report(), a)
        self.assertEqual(len(p["verification"]), 1)
        self.assertEqual(p["verification"][0]["kind"], "doctor_then_representative_probe")


if __name__ == "__main__":
    unittest.main()
