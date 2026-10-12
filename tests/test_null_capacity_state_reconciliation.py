import unittest

from analysis.null_capacity_state_reconciliation import build_report


class NullCapacityStateReconciliationV2Tests(unittest.TestCase):
    def fixtures(self, strict_fraction=0.937, canonical_fraction=0.947, gate_fraction=0.947):
        strict = {"stochastic_null_protocol": {"model_capacity_review": {
            "surrogate_boundary_fraction": strict_fraction,
            "observed_selected_order": 20,
            "maximum_declared_order": 20,
        }}}
        canonical = {"metadata": {"seed": 42}, "appropriate_stochastic_null": {
            "selected_order": 20,
            "order_selection_diagnostic": {"surrogate_boundary_fraction": canonical_fraction},
        }}
        gate = {"canonical_null_diagnostics": {
            "selected_order": 20,
            "surrogate_boundary_fraction": gate_fraction,
        }, "protocol": {"max_order": 20, "protocol_revision": "ar_order_comparison_holdback_v1"}}
        audit = {
            "surrogate_boundary_fraction": strict_fraction,
            "observed_selected_order": 20,
            "max_order": 20,
            "seed": 90210,
            "protocol_revision": "ar_order_comparison_holdback_v1",
        }
        return strict, canonical, gate, audit

    def test_different_source_estimates_are_reconciled_by_source(self):
        strict, canonical, gate, audit = self.fixtures()
        report = build_report(strict, canonical, gate, audit)
        self.assertEqual(report["status"], "SOURCE_SCOPED_ESTIMATES_RECONCILED")
        self.assertTrue(report["comparisons"]["strict_claim_matches_primary_audit_fraction_within_1e-12"])
        self.assertTrue(report["comparisons"]["canonical_report_matches_null_gate_fraction_within_1e-12"])
        self.assertAlmostEqual(report["cross_source_fraction_difference"], -0.01)
        self.assertFalse(report["claim_support"])
        self.assertFalse(report["promotion_authority"])
        self.assertFalse(report["scientific_inputs_modified"])

    def test_primary_audit_mismatch_remains_reconciliation_required(self):
        strict, canonical, gate, audit = self.fixtures()
        audit["surrogate_boundary_fraction"] = 0.938
        report = build_report(strict, canonical, gate, audit)
        self.assertEqual(report["status"], "RECONCILIATION_REQUIRED")
        self.assertFalse(report["comparisons"]["strict_claim_matches_primary_audit_fraction_within_1e-12"])

    def test_missing_primary_audit_does_not_silently_pass(self):
        strict, canonical, gate, _ = self.fixtures()
        report = build_report(strict, canonical, gate, None)
        self.assertEqual(report["status"], "RECONCILIATION_REQUIRED_PRIMARY_AUDIT_MISSING")
        self.assertFalse(report["claim_support"])
        self.assertFalse(report["promotion_authority"])

    def test_canonical_gate_mismatch_remains_reconciliation_required(self):
        strict, canonical, gate, audit = self.fixtures()
        gate["canonical_null_diagnostics"]["surrogate_boundary_fraction"] = 0.946
        report = build_report(strict, canonical, gate, audit)
        self.assertEqual(report["status"], "RECONCILIATION_REQUIRED")


if __name__ == "__main__":
    unittest.main()
