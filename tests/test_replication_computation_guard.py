import unittest
from unittest.mock import patch

from analysis.replication_computation_guard import (
    REQUIRED_PROVENANCE_FIELDS,
    candidate_computation_gate,
    protocol_freeze_state,
)
from scripts import canonical_consensus
from analysis import independent_domain_replication_gate as replication_gate
from analysis import cross_domain_band_guard


def candidate(path="real-data/hadcet_monthly.csv", approved=True):
    value = {
        "path": path,
        "replication_eligible": approved,
        "explicit_approval": approved,
    }
    for field in REQUIRED_PROVENANCE_FIELDS:
        value[field] = "documented"
    value["known_shared_nuisance_with_primary"] = (
        "Assessment completed; shared nuisance sources and decision documented."
    )
    return value


def frozen_claim():
    return {
        "stochastic_null_protocol": {
            "status": "confirmatory_protocol_frozen",
            "preregistered_confirmation": True,
            "confirmatory_status": {
                "status": "frozen",
                "confirmatory_null_frozen": True,
            },
        }
    }


class ReplicationComputationGuardTests(unittest.TestCase):
    def test_current_exploratory_protocol_is_not_frozen(self):
        claim = {
            "stochastic_null_protocol": {
                "status": "post_observation_protocol_amendment_not_confirmatory",
                "preregistered_confirmation": False,
                "confirmatory_status": {
                    "status": "not_frozen",
                    "confirmatory_null_frozen": False,
                },
            }
        }
        frozen, reasons = protocol_freeze_state(claim)
        self.assertFalse(frozen)
        self.assertIn("confirmatory_null_not_frozen", reasons)
        self.assertIn("prospective_preregistration_not_confirmed", reasons)

    def test_approval_alone_cannot_bypass_unfrozen_protocol(self):
        allowed, reasons = candidate_computation_gate(
            candidate(approved=True),
            "real-data/hadcet_monthly.csv",
            protocol_frozen=False,
        )
        self.assertFalse(allowed)
        self.assertIn("confirmatory_protocol_not_frozen", reasons)

    def test_explicit_approval_is_required_even_when_protocol_is_frozen(self):
        item = candidate(approved=True)
        item.pop("explicit_approval")
        allowed, reasons = candidate_computation_gate(
            item,
            "real-data/hadcet_monthly.csv",
            protocol_frozen=True,
        )
        self.assertFalse(allowed)
        self.assertIn("explicit_approval_missing", reasons)

    def test_pending_provenance_cannot_be_approved_by_boolean_flags(self):
        item = candidate(approved=True)
        item["known_shared_nuisance_with_primary"] = (
            "PENDING_REVIEW: assess shared nuisance structure"
        )
        allowed, reasons = candidate_computation_gate(
            item,
            "real-data/hadcet_monthly.csv",
            protocol_frozen=True,
        )
        self.assertFalse(allowed)
        self.assertIn("incomplete_provenance_metadata", reasons)
        self.assertIn(
            "missing_provenance_field:known_shared_nuisance_with_primary",
            reasons,
        )

    def test_unapproved_secondary_never_reaches_alpha_estimator(self):
        spec = {
            "name": "hadcet_monthly",
            "path": "real-data/hadcet_monthly.csv",
            "role": "independent_real",
            "independent": True,
            "derived_from": None,
        }
        policy = {
            "minimum_series_length": 256,
            "estimator_minimum_series_length": 512,
            "replication_minimum_series_length": 1024,
            "minimum_frequency_bins": 20,
            "canonical_nperseg": 1024,
            "freq_min": 0.01,
            "freq_max": 0.05,
        }
        with patch.object(canonical_consensus, "load_series") as load_series, \
             patch.object(canonical_consensus, "estimate_alpha") as estimate_alpha:
            result = canonical_consensus.evaluate_dataset(
                spec,
                policy,
                candidate=candidate(approved=False),
                protocol_frozen=False,
            )
        load_series.assert_not_called()
        estimate_alpha.assert_not_called()
        self.assertIsNone(result["alpha"])
        self.assertEqual(result["computation_status"], "SKIPPED")

    def test_replication_gate_does_not_call_evaluator_if_protocol_unfrozen(self):
        policy = {
            "confirmatory_protocol_frozen": False,
            "protocol_freeze_reasons": ["confirmatory_null_not_frozen"],
        }
        with patch.object(replication_gate, "evaluate_domain") as evaluate_domain:
            result = replication_gate.evaluate_candidate_if_approved(
                "hadcet_monthly",
                candidate(approved=True),
                policy,
                123,
            )
        evaluate_domain.assert_not_called()
        self.assertEqual(result["replication_status"], "SKIPPED_PROTOCOL_NOT_FROZEN")
        self.assertEqual(result["computation_status"], "SKIPPED")

    def test_cross_domain_main_skips_without_calling_alpha(self):
        import tempfile
        from pathlib import Path

        fake_inputs = {
            "claim": {},
            "candidates": {
                "hadcet_monthly": candidate(),
                "fred_indpro": candidate("real-data/fred_indpro_monthly.csv"),
            },
            "protocol_frozen": False,
            "protocol_freeze_reasons": ["confirmatory_null_not_frozen"],
            "minimum_series_length": 256,
            "estimator_minimum_series_length": 512,
            "replication_minimum_series_length": 1024,
            "minimum_frequency_bins": 20,
            "canonical_nperseg": 1024,
            "freq_min": 0.01,
            "freq_max": 0.05,
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(cross_domain_band_guard, "load_inputs", return_value=fake_inputs), \
                 patch.object(cross_domain_band_guard, "DATASETS", {
                     "sunspots": "real-data/sunspots_full.csv",
                     "hadcet_monthly": "real-data/hadcet_monthly.csv",
                     "fred_indpro": "real-data/fred_indpro_monthly.csv",
                 }), \
                 patch.object(cross_domain_band_guard, "OUTPUT", Path(tmp) / "report.json"), \
                 patch.object(cross_domain_band_guard, "estimate_alpha") as estimate_alpha:
                cross_domain_band_guard.main()
                estimate_alpha.assert_not_called()

    def test_cross_domain_guard_has_no_eligible_candidates_until_protocol_frozen(self):
        inputs = {
            "candidates": {
                "hadcet_monthly": candidate(),
                "fred_indpro": candidate("real-data/fred_indpro_monthly.csv"),
            },
            "protocol_frozen": False,
        }
        with patch.object(cross_domain_band_guard, "DATASETS", {
            "sunspots": "real-data/sunspots_full.csv",
            "hadcet_monthly": "real-data/hadcet_monthly.csv",
            "fred_indpro": "real-data/fred_indpro_monthly.csv",
        }):
            approved, excluded = cross_domain_band_guard.eligible_secondary_candidates(inputs)
        self.assertEqual(approved, [])
        self.assertEqual(len(excluded), 2)


if __name__ == "__main__":
    unittest.main()
