import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ek_doctor", ROOT / "scripts" / "doctor.py")
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def load_wechat_provider():
    adapter = json.loads(
        (ROOT / "adapters" / "zcode-v0.3-beta.1.json").read_text(encoding="utf-8")
    )
    for capability in adapter["capabilities"]:
        if capability.get("id") == "wechat.discovery":
            for provider in capability.get("providers", []):
                if provider.get("id") == "wechat-article-search":
                    return provider
    raise AssertionError("wechat.discovery/wechat-article-search not found")


def diagnose_provider(provider):
    adapter = {
        "adapter_id": "zcode-path-regression",
        "capabilities": [{"id": "wechat.discovery", "providers": [provider]}],
    }
    report = mod.diagnose(adapter, {}, {})
    return report["capabilities"][0]["providers"][0]


class ZCodeAdapterPathTests(unittest.TestCase):
    def test_adapter_declares_both_evidenced_candidate_paths(self):
        provider = load_wechat_provider()
        values = [check["value"] for check in provider["checks"]]
        self.assertEqual(
            values,
            [
                "~/.zcode/skills/wechat-article-search/scripts/search_wechat.js",
                "~/.codex/skills/wechat-article-search/scripts/search_wechat.js",
            ],
        )
        self.assertTrue(all(check["exposure_class"] == "local_script" for check in provider["checks"]))
        self.assertTrue(all(check["absence_authoritative"] for check in provider["checks"]))

    def test_zcode_present_codex_absent_blocks_missing_without_promoting_available(self):
        provider = load_wechat_provider()

        def exists(path):
            normalized = str(path).replace("\\", "/")
            return normalized.endswith(
                "/.zcode/skills/wechat-article-search/scripts/search_wechat.js"
            )

        with mock.patch.object(mod.Path, "exists", autospec=True, side_effect=exists):
            result = diagnose_provider(provider)

        self.assertEqual(result["operational_status"], "UNKNOWN")
        self.assertEqual(result["exposure_merge"]["conflicting_present_classes"], ["local_script"])
        self.assertNotEqual(result["operational_status"], "AVAILABLE")
        self.assertNotEqual(result["operational_status"], "MISSING_CONFIRMED")

    def test_both_candidate_paths_absent_confirms_local_script_missing(self):
        provider = load_wechat_provider()
        with mock.patch.object(mod.Path, "exists", autospec=True, return_value=False):
            result = diagnose_provider(provider)

        self.assertEqual(result["operational_status"], "MISSING_CONFIRMED")
        self.assertEqual(result["exposure_merge"]["authoritative_absent_classes"], ["local_script"])
        self.assertEqual(result["exposure_merge"]["uncovered_legal_classes"], [])


if __name__ == "__main__":
    unittest.main()
