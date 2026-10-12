import unittest

from analysis.eligibility_diagnostic_labels import enrich_domain, enrich_report


class EligibilityDiagnosticLabelsTests(unittest.TestCase):
    def test_primary_domain_role_exclusion_supersedes_irrelevant_missing_provenance(self):
        source = {
            "name": "sunspots", "eligible_for_measurement": True,
            "eligible_for_replication": False, "provenance_replication_eligible": False,
            "primary_domain": True, "derived_domain": False,
            "reason": "eligible", "replication_exclusion_reason": "primary_domain_excluded_from_secondary_replication_count",
            "provenance_exclusion_reason": "missing_provenance_registry_entry",
        }
        result = enrich_domain(source)
        self.assertEqual(result["diagnostic_labels"]["structural_status"], "MEASUREMENT_VALID")
        self.assertEqual(result["diagnostic_labels"]["final_replication_status"], "EXCLUDED_PRIMARY_DOMAIN")
        self.assertEqual(result["diagnostic_labels"]["final_replication_reasons"], ["primary_domain_excluded_from_secondary_replication_count"])
        self.assertFalse(result["eligible_for_replication"])
        self.assertEqual(result["provenance_exclusion_reason"], "missing_provenance_registry_entry")

    def test_derived_domain_remains_excluded_by_role(self):
        result = enrich_domain({
            "name": "extended", "eligible_for_measurement": True,
            "eligible_for_replication": False, "provenance_replication_eligible": False,
            "primary_domain": False, "derived_domain": True,
        })
        self.assertEqual(result["diagnostic_labels"]["final_replication_status"], "EXCLUDED_DERIVED_DOMAIN")
        self.assertEqual(result["diagnostic_labels"]["final_replication_reasons"], ["derived_or_related_domain_excluded"])
        self.assertFalse(result["eligible_for_replication"])

    def test_structurally_valid_but_unapproved_secondary_stays_ineligible(self):
        result = enrich_domain({
            "name": "hadcet_monthly", "eligible_for_measurement": True,
            "eligible_for_replication": False, "provenance_replication_eligible": False,
            "primary_domain": False, "derived_domain": False,
            "reason": "eligible",
            "replication_exclusion_reason": "dataset_passed_structural_eligibility_but_failed_replication_provenance_eligibility",
            "provenance_exclusion_reason": "provenance_not_approved_for_replication",
            "provenance_review": {"reason": "Candidate only; independence review pending."},
        })
        self.assertEqual(result["diagnostic_labels"]["structural_status"], "MEASUREMENT_VALID")
        self.assertEqual(result["diagnostic_labels"]["final_replication_status"], "NOT_REPLICATION_ELIGIBLE")
        self.assertIn("provenance_not_approved_for_replication", result["diagnostic_labels"]["final_replication_reasons"])
        self.assertFalse(result["eligible_for_replication"])

    def test_report_count_and_status_are_preserved(self):
        source = {
            "status": "REPLICATION_ELIGIBILITY_INSUFFICIENT",
            "eligible_replication_domain_count": 0,
            "domains": [{"name": "x", "eligible_for_measurement": True,
                         "eligible_for_replication": False, "primary_domain": True}],
        }
        result = enrich_report(source)
        self.assertEqual(result["status"], source["status"])
        self.assertEqual(result["eligible_replication_domain_count"], 0)
        self.assertFalse(result["existing_gate_decisions_modified"])
        self.assertFalse(result["domains"][0]["eligible_for_replication"])


if __name__ == "__main__":
    unittest.main()
