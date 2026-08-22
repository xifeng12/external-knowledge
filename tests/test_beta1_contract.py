import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Beta1ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = json.loads(
            (ROOT / "adapters" / "zcode-v0.3-beta.1.json").read_text(encoding="utf-8")
        )

    def _cap(self, cap_id):
        return next(c for c in self.adapter["capabilities"] if c["id"] == cap_id)

    def test_wechat_provider_uses_local_script_not_skill_or_network_as_exposure(self):
        cap = self._cap("wechat.discovery")
        p = cap["providers"][0]
        self.assertEqual(p["id"], "wechat-article-search")
        self.assertEqual(p["exposure_contract"]["legal_classes"], ["local_script"])
        self.assertNotIn("skill_registry", p["exposure_contract"]["legal_classes"])
        self.assertNotIn("network_execution", p["exposure_contract"]["legal_classes"])

    def test_wechat_script_check_is_binding_scoped(self):
        p = self._cap("wechat.discovery")["providers"][0]
        check = p["checks"][0]
        self.assertEqual(check["type"], "path")
        self.assertEqual(check["exposure_class"], "local_script")
        self.assertEqual(check["carrier_class"], "skill_registry")
        self.assertTrue(check["absence_authoritative"])
        self.assertIn("search_wechat.js", check["value"])

    def test_node_cheerio_and_sogou_are_dependencies_not_exposure_classes(self):
        p = self._cap("wechat.discovery")["providers"][0]
        kinds = {d["kind"] for d in p["runtime_dependencies"]}
        self.assertEqual(kinds, {"runtime", "bundled_dependency", "network_backend"})
        legal = set(p["exposure_contract"]["legal_classes"])
        for forbidden in {"runtime", "bundled_dependency", "network_backend"}:
            self.assertNotIn(forbidden, legal)

    def test_source_semantic_profile_separates_specialist_and_general_web_discoverability(self):
        profile = next(
            x for x in self.adapter["source_semantic_profiles"]
            if x["source_semantic"] == "wechat.article-discovery"
        )
        by_ref = {p["provider_ref"]: p for p in profile["providers"]}
        specialist = by_ref["wechat.discovery/wechat-article-search"]
        fallback = by_ref["general-web.search/runtime-native.web-search"]
        self.assertEqual(specialist["discoverability"], "LIMITED_OBSERVED")
        self.assertEqual(specialist["semantic_coverage"], "EQUIVALENT")
        self.assertEqual(fallback["discoverability"], "VERY_LOW_OBSERVED")
        self.assertEqual(fallback["semantic_coverage"], "DEGRADED")
        self.assertEqual(fallback["evidence_strength"], "REPEATED_ACROSS_CASES")

    def test_retrieval_quality_contract_has_required_stop_signals(self):
        text = (ROOT / "references" / "retrieval-quality.md").read_text(encoding="utf-8")
        self.assertIn("LOW_QUERY_DISCRIMINATION", text)
        self.assertIn("one contextual rewrite", text)
        self.assertIn("Provider × Source Semantic", text)
        self.assertIn("VERY_LOW_OBSERVED", text)
        self.assertIn("provider callable", text)

    def test_runtime_note_does_not_promote_reader_fallback_to_portable_rule(self):
        text = (ROOT / "references" / "runtime-notes-zcode.md").read_text(encoding="utf-8")
        self.assertIn("OBSERVED_IN_RUNTIME", text)
        self.assertIn("Do not turn it into a portable requirement", text)
        self.assertIn("ctx_fetch_and_index", text)


if __name__ == "__main__":
    unittest.main()
