import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentInventoryReferenceTests(unittest.TestCase):
    def test_reference_documents_current_inventory_contract(self):
        text = (ROOT / "references" / "agent-inventory.md").read_text(encoding="utf-8")
        for token in [
            "inventory_version: 4",
            "AVAILABLE_WITH_SCOPE",
            "MISSING_CONFIRMED",
            "authoritative_for_absence",
            "absence_covers_exposure_classes",
            "exposure_class",
            "carrier_class",
            "scripts/inventory_scaffold.py",
        ]:
            self.assertIn(token, text)

    def test_machine_diagnostics_links_inventory_reference(self):
        text = (ROOT / "references" / "machine-diagnostics.md").read_text(encoding="utf-8")
        self.assertIn("references/agent-inventory.md", text)


if __name__ == "__main__":
    unittest.main()
