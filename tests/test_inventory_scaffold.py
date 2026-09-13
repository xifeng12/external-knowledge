import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ek_inventory_scaffold", ROOT / "scripts" / "inventory_scaffold.py"
)
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class InventoryScaffoldTests(unittest.TestCase):
    def adapter(self):
        return {
            "adapter_id": "test-adapter",
            "capabilities": [
                {
                    "id": "general-web.read",
                    "providers": [
                        {
                            "id": "native",
                            "exposure_contract": {
                                "legal_classes": ["native_tool"]
                            },
                        }
                    ],
                },
                {
                    "id": "complex-web.read",
                    "providers": [
                        {
                            "id": "firecrawl",
                            "exposure_contract": {
                                "legal_classes": ["path_cli", "mcp", "mcp"]
                            },
                        }
                    ],
                },
            ],
        }

    def test_scaffold_is_deterministic_and_non_evidentiary(self):
        first = mod.build_scaffold(self.adapter())
        second = mod.build_scaffold(self.adapter())
        self.assertEqual(first, second)
        self.assertEqual(first["inventory_version"], 4)
        self.assertEqual(first["runtime"], "unknown")

        for capability in first["capabilities"].values():
            for provider in capability["providers"].values():
                self.assertEqual(provider["status"], "UNKNOWN")
                self.assertFalse(provider["authoritative_for_absence"])
                self.assertEqual(provider["absence_covers_exposure_classes"], [])
                self.assertNotIn(provider["status"], {"AVAILABLE", "MISSING_CONFIRMED"})

    def test_declared_legal_classes_are_guidance_not_absence_claims(self):
        scaffold = mod.build_scaffold(self.adapter())
        firecrawl = scaffold["capabilities"]["complex-web.read"]["providers"]["firecrawl"]
        self.assertEqual(firecrawl["declared_legal_exposure_classes"], ["mcp", "path_cli"])
        self.assertEqual(firecrawl["absence_covers_exposure_classes"], [])
        self.assertFalse(firecrawl["authoritative_for_absence"])

    def test_cli_output_matches_builder_and_writes_requested_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            adapter_path = root / "adapter.json"
            output_path = root / "inventory.json"
            adapter_path.write_text(json.dumps(self.adapter()), encoding="utf-8")

            rc = mod.main([
                "--adapter", str(adapter_path),
                "--pretty",
                "--output", str(output_path),
            ])
            self.assertEqual(rc, 0)
            written = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(written, mod.build_scaffold(self.adapter()))


if __name__ == "__main__":
    unittest.main()
