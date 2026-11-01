import unittest

from scripts.type1_occurrence_classifier import classify_occurrence


def ctx(*items):
    return [
        {"line": number, "text": text}
        for number, text in items
    ]


class OccurrenceLocalClassifierTests(unittest.TestCase):

    def classify(self, text, context, line=10, path="protocol/example.md"):
        return classify_occurrence(
            path=path,
            line=line,
            matched_text=text,
            context_window=context,
        )

    def test_historical_is_detected_from_local_context(self):
        result = self.classify(
            "0.075",
            ctx(
                (8, "Historical result from the prior run."),
                (10, "Upper limit: 0.075"),
            ),
        )
        self.assertEqual(result["suggested_classification"], "HISTORICAL")

    def test_proposal_is_detected_from_local_context(self):
        result = self.classify(
            "0.075",
            ctx(
                (9, "Candidate proposal; not approved."),
                (10, "Upper limit: 0.075"),
            ),
        )
        self.assertEqual(result["suggested_classification"], "PROPOSAL")

    def test_diagnostic_is_detected_from_local_context(self):
        result = self.classify(
            "0.075",
            ctx(
                (10, "Diagnostic audit only: 0.075"),
            ),
        )
        self.assertEqual(result["suggested_classification"], "DIAGNOSTIC")

    def test_governance_is_occurrence_specific(self):
        result = self.classify(
            "confirmatory_execution_authorized",
            ctx(
                (9, "Authorization guard"),
                (10, "confirmatory_execution_authorized"),
            ),
        )
        self.assertEqual(result["suggested_classification"], "GOVERNANCE")

    def test_runner_candidate_is_not_declared_gated(self):
        result = self.classify(
            "python -m analysis.calibrate_null_type1",
            ctx(
                (10, "python -m analysis.calibrate_null_type1"),
                (11, "exit 1"),
            ),
            path=".github/workflows/example.yml",
        )
        self.assertEqual(
            result["suggested_classification"],
            "EXECUTION_PATH_CANDIDATE_UNVERIFIED",
        )
        self.assertFalse(result["evidence"]["guard_order_verified"])

    def test_distant_runner_does_not_change_occurrence_classification(self):
        result = self.classify(
            "0.075",
            ctx(
                (1, "python -m analysis.calibrate_null_type1"),
                (10, "Upper limit: 0.075"),
                (20, "Unrelated workflow documentation"),
            ),
        )
        self.assertEqual(result["suggested_classification"], "UNKNOWN")

    def test_context_outside_radius_is_ignored(self):
        result = self.classify(
            "0.075",
            ctx(
                (4, "Historical result"),
                (10, "Upper limit: 0.075"),
            ),
        )
        self.assertEqual(result["suggested_classification"], "UNKNOWN")

    def test_unknown_is_preserved_when_context_is_insufficient(self):
        result = self.classify(
            "0.075",
            ctx((10, "Upper limit: 0.075")),
        )
        self.assertEqual(result["suggested_classification"], "UNKNOWN")
        self.assertEqual(result["manual_classification"], "UNKNOWN")
        self.assertEqual(result["status"], "OPEN")

    def test_classifier_never_closes_or_authorizes(self):
        result = self.classify(
            "confirmatory_execution_authorized",
            ctx((10, "confirmatory_execution_authorized")),
        )
        self.assertEqual(result["manual_classification"], "UNKNOWN")
        self.assertEqual(result["status"], "OPEN")
        self.assertEqual(result["reviewer_disposition"], "PENDING")
        self.assertFalse(result["execution_authority"])
        self.assertFalse(result["classification_is_human_adjudication"])

    def test_invalid_line_is_rejected(self):
        with self.assertRaises(ValueError):
            self.classify("0.075", ctx((10, "0.075")), line=True)

    def test_invalid_context_line_is_rejected(self):
        with self.assertRaises(ValueError):
            self.classify(
                "0.075",
                [{"line": True, "text": "0.075"}],
            )

    def test_missing_context_remains_unknown(self):
        result = classify_occurrence(
            path="protocol/example.md",
            line=10,
            matched_text="unclassified reference",
            context_window=None,
        )
        self.assertEqual(result["suggested_classification"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main(verbosity=2)
