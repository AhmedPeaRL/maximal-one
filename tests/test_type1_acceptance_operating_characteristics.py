import unittest

from analysis.type1_acceptance_operating_characteristics import (
    accepted_counts,
    binomial_probabilities,
    summarize,
    wilson_interval,
)


class TypeIAcceptanceOperatingCharacteristicsTests(unittest.TestCase):
    def test_wilson_boundary_matches_declared_cutoff(self):
        self.assertLessEqual(wilson_interval(58, 1000)[1], 0.075)
        self.assertGreater(wilson_interval(59, 1000)[1], 0.075)

    def test_accepted_counts_are_zero_through_58(self):
        accepted = accepted_counts(1000, 0.075)
        self.assertEqual(accepted[0], 0)
        self.assertEqual(accepted[-1], 58)
        self.assertEqual(len(accepted), 59)

    def test_binomial_probabilities_normalize(self):
        probabilities = binomial_probabilities(1000, 0.05)
        self.assertAlmostEqual(sum(probabilities), 1.0, places=12)

    def test_expected_operating_characteristics(self):
        result = summarize()
        self.assertAlmostEqual(result["false_fail_probability_one_nominal_scenario"], 0.11056, delta=0.0001)
        self.assertAlmostEqual(result["probability_at_least_one_false_fail_if_scenarios_independent"], 0.37416, delta=0.0001)
        self.assertAlmostEqual(result["exact_binomial_upper_tail_examples"]["60"], 0.08673, delta=0.0001)
        self.assertAlmostEqual(result["exact_binomial_upper_tail_examples"]["73"], 0.001006, delta=0.00001)


if __name__ == "__main__":
    unittest.main()
