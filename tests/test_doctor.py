import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ek_doctor", ROOT / "scripts" / "doctor.py")
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def provider(pid="p", legal=None, checks=None, coverage="EQUIVALENT"):
    return {
        "id": pid,
        "coverage_grade": coverage,
        "checks": checks or [],
        "exposure_contract": {
            "legal_classes": legal or [],
            "scope": "test runtime",
        },
    }


def capability(providers):
    return {"id": "x", "providers": providers}


def inventory(entries):
    return {
        "runtime": "test",
        "capabilities": {
            "x": {"providers": entries}
        },
    }


class DoctorAlpha2Tests(unittest.TestCase):
    def diagnose(self, providers, entries=None, need="WANTED", fallback="NO"):
        adapter = {"adapter_id": "t", "capabilities": [capability(providers)]}
        agent = inventory(entries or {})
        needs = {"needs": {"x": {"level": need, "equivalent_fallback": fallback}}}
        return mod.diagnose(adapter, agent, needs)["capabilities"][0]

    def test_plugin_to_mcp_carrier_not_double_counted(self):
        p = provider(
            legal=["mcp"],
            checks=[{
                "type": "path",
                "value": "__definitely_missing_plugin_manifest__",
                "exposure_class": "mcp",
                "carrier_class": "plugin_registry",
                "absence_authoritative": True,
            }],
        )
        c = self.diagnose([p], need="NOT_NEEDED")
        pr = c["providers"][0]
        self.assertEqual(pr["operational_status"], "MISSING_CONFIRMED")
        self.assertEqual(pr["exposure_merge"]["legal_exposure_classes"], ["mcp"])
        self.assertEqual(pr["exposure_merge"]["carrier_classes_observed"], ["plugin_registry"])

    def test_skill_to_cli_carrier_not_double_counted(self):
        with mock.patch.object(mod.shutil, "which", return_value=None):
            p = provider(
                legal=["path_cli"],
                checks=[{
                    "type": "command",
                    "value": "toolx",
                    "exposure_class": "path_cli",
                    "carrier_class": "skill_registry",
                    "absence_authoritative": True,
                }],
            )
            c = self.diagnose([p])
            pr = c["providers"][0]
            self.assertEqual(pr["operational_status"], "MISSING_CONFIRMED")
            self.assertEqual(pr["exposure_merge"]["legal_exposure_classes"], ["path_cli"])
            self.assertEqual(pr["exposure_merge"]["carrier_classes_observed"], ["skill_registry"])

    def test_path_absence_is_scoped_authoritative_when_declared(self):
        with mock.patch.object(mod.shutil, "which", return_value=None):
            p = provider(
                legal=["path_cli"],
                checks=[{
                    "type": "command",
                    "value": "firecrawl",
                    "exposure_class": "path_cli",
                    "absence_authoritative": True,
                }],
            )
            c = self.diagnose([p])
            pr = c["providers"][0]
            self.assertEqual(pr["operational_status"], "MISSING_CONFIRMED")
            ev = pr["evidence"][0]
            self.assertTrue(ev["authoritative_for_absence"])
            self.assertIn("current process PATH", ev["scope"])

    def test_path_present_does_not_establish_provider_available(self):
        with mock.patch.object(mod.shutil, "which", return_value="/fake/firecrawl"):
            p = provider(
                legal=["path_cli"],
                checks=[{
                    "type": "command",
                    "value": "firecrawl",
                    "exposure_class": "path_cli",
                    "absence_authoritative": True,
                }],
            )
            c = self.diagnose([p])
            pr = c["providers"][0]
            self.assertEqual(pr["operational_status"], "UNKNOWN")
            self.assertIn("path_cli", pr["exposure_merge"]["conflicting_present_classes"])

    def test_provider_missing_does_not_make_capability_missing_when_other_provider_available(self):
        p1 = provider("native", ["native_tool"], coverage="DEGRADED")
        p2 = provider("firecrawl", ["mcp"], coverage="EQUIVALENT")
        entries = {
            "native": {
                "status": "AVAILABLE",
                "evidence_kind": "runtime_tool_exposure",
                "scope": "test",
            },
            "firecrawl": {
                "status": "UNKNOWN",
                "evidence_kind": "registry_inventory",
                "scope": "mcp",
                "authoritative_for_absence": True,
                "absence_covers_exposure_classes": ["mcp"],
            },
        }
        c = self.diagnose([p1, p2], entries=entries)
        self.assertEqual(c["providers"][1]["operational_status"], "MISSING_CONFIRMED")
        self.assertEqual(c["operational_status"], "AVAILABLE_WITH_SCOPE")
        self.assertEqual(c["best_provider"], "native")

    def test_capability_missing_only_if_all_providers_missing(self):
        p1 = provider("a", ["mcp"])
        p2 = provider("b", ["path_cli"])
        entries = {
            "a": {
                "status": "UNKNOWN",
                "authoritative_for_absence": True,
                "absence_covers_exposure_classes": ["mcp"],
            },
            "b": {
                "status": "UNKNOWN",
                "authoritative_for_absence": True,
                "absence_covers_exposure_classes": ["path_cli"],
            },
        }
        c = self.diagnose([p1, p2], entries=entries)
        self.assertEqual(c["operational_status"], "MISSING_CONFIRMED")

    def test_unknown_provider_keeps_capability_unknown_if_none_available(self):
        p1 = provider("a", ["mcp"])
        p2 = provider("b", ["path_cli"])
        entries = {
            "a": {
                "status": "UNKNOWN",
                "authoritative_for_absence": True,
                "absence_covers_exposure_classes": ["mcp"],
            }
        }
        c = self.diagnose([p1, p2], entries=entries)
        self.assertEqual(c["providers"][0]["operational_status"], "MISSING_CONFIRMED")
        self.assertEqual(c["providers"][1]["operational_status"], "UNKNOWN")
        self.assertEqual(c["operational_status"], "UNKNOWN")

    def test_equivalent_available_provider_makes_capability_available(self):
        p = provider("p", ["native_tool"], coverage="EQUIVALENT")
        c = self.diagnose([p], entries={
            "p": {
                "status": "AVAILABLE",
                "evidence_kind": "representative_probe",
                "scope": "test",
            }
        })
        self.assertEqual(c["operational_status"], "AVAILABLE")
        self.assertEqual(c["plan_action"], "KEEP")

    def test_not_needed_capability_never_install_candidate(self):
        p = provider("p", ["mcp"])
        c = self.diagnose([p], entries={
            "p": {
                "status": "UNKNOWN",
                "authoritative_for_absence": True,
                "absence_covers_exposure_classes": ["mcp"],
            }
        }, need="NOT_NEEDED", fallback="NO")
        self.assertEqual(c["operational_status"], "MISSING_CONFIRMED")
        self.assertEqual(c["plan_action"], "DO_NOT_INSTALL")

    def test_doctor_never_marks_environment_mutation(self):
        r = mod.diagnose({"adapter_id": "t", "capabilities": []}, {}, {})
        self.assertFalse(r["environment_mutation_attempted"])


if __name__ == "__main__":
    unittest.main()
