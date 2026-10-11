import unittest

from analysis.null_capacity_state_reconciliation import build_report


class NullCapacityStateReconciliationTests(unittest.TestCase):
    def fixtures(self, strict_fraction=0.937, canonical_fraction=0.947, gate_fraction=0.947):
        strict = {"stochastic_null_protocol": {"model_capacity_review": {
            "surrogate_boundary_fraction": strict_fraction,
            "observed_selected_order": 20,
            "maximum_declared_order": 20,
        }}}
        canonical = {"appropriate_stochastic_null": {
            "selected_order": 20,
            "order_selection_diagnostic": {"surrogate_boundary_fraction": canonical_fraction},
        }}
        gate = {"canonical_null_diagnostics": {
            "selected_order": 20,
            "surrogate_boundary_fraction": gate_fraction,
        }, "protocol": {"max_order": 20}}
        return strict, canonical, gate

    def test_records_boundary_fraction_discrepancy_without_authority(self):
        report = build_report(*self.fixtures())
        self.assertEqual(report["status"], "RECONCILIATION_REQUIRED")
        self.assertFalse(report["claim_support"])
        self.assertFalse(report["promotion_authority"])
        self.assertFalse(report["scientific_inputs_modified"])
        self.assertFalse(report["comparisons"]["boundary_fraction_match_within_1e-12"])

    def test_matching_fields_are_reported_as_match(self):
        report = build_report(*self.fixtures(0.947, 0.947, 0.947))
        self.assertEqual(report["status"], "MATCH")
        self.assertTrue(report["comparisons"]["boundary_fraction_match_within_1e-12"])
        self.assertTrue(report["comparisons"]["selected_order_match"])
        self.assertTrue(report["comparisons"]["maximum_order_match"])

    def test_missing_values_require_reconciliation(self):
        strict, canonical, gate = self.fixtures()
        canonical["appropriate_stochastic_null"]["order_selection_diagnostic"].pop("surrogate_boundary_fraction")
        report = build_report(strict, canonical, gate)
        self.assertEqual(report["status"], "RECONCILIATION_REQUIRED")
        self.assertIsNone(report["comparisons"]["boundary_fraction_match_within_1e-12"])

    def test_different_selected_order_is_detected(self):
        strict, canonical, gate = self.fixtures(0.947, 0.947, 0.947)
        gate["canonical_null_diagnostics"]["selected_order"] = 19
        report = build_report(strict, canonical, gate)
        self.assertEqual(report["status"], "RECONCILIATION_REQUIRED")
        self.assertFalse(report["comparisons"]["selected_order_match"])


if __name__ == "__main__":
    unittest.main()
