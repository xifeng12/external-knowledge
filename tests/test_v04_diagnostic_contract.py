import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class V04DiagnosticContractTests(unittest.TestCase):
    def test_capability_map_keeps_repository_and_machine_state_separate(self):
        text = (ROOT / "references" / "capability-map.md").read_text(encoding="utf-8")
        self.assertIn("Repository Capability Map", text)
        self.assertIn("Machine Capability Receipt", text)
        self.assertIn("Skill presence alone is never promoted to `AVAILABLE`", text)

    def test_machine_diagnostics_requires_explicit_roots_and_explicit_claims(self):
        text = (ROOT / "references" / "machine-diagnostics.md").read_text(encoding="utf-8")
        self.assertIn("Roots are explicit by design", text)
        self.assertIn("claim_status = DECLARED_ONLY", text)
        self.assertIn("capability_attribution = UNCLASSIFIED", text)
        self.assertIn("does not execute Skill code", text)


if __name__ == "__main__":
    unittest.main()
