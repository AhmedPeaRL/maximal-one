import unittest

from analysis.type1_acceptance_operating_characteristics import (
    accepted_counts,
    binomial_probabilities,
    summarize,
    wilson_interval,
)


class TypeIAcceptanceOperatingCharacteristicsTests(unittest.TestCase):
    def test_production_rule_requires_interval_to_contain_nominal_rate(self):
        self.assertLess(wilson_interval(36, 1000)[1], 0.05)
        self.assertLessEqual(wilson_interval(37, 1000)[0], 0.05)
        self.assertGreaterEqual(wilson_interval(37, 1000)[1], 0.05)
        self.assertEqual(accepted_counts(1000, 0.05, 0.075)[0], 37)

    def test_production_rule_upper_boundary(self):
        self.assertLessEqual(wilson_interval(58, 1000)[1], 0.075)
        self.assertGreater(wilson_interval(59, 1000)[1], 0.075)
        accepted = accepted_counts(1000, 0.05, 0.075)
        self.assertEqual(accepted, list(range(37, 59)))

    def test_binomial_probabilities_normalize(self):
        probabilities = binomial_probabilities(1000, 0.05)
        self.assertAlmostEqual(sum(probabilities), 1.0, places=12)

    def test_operating_characteristics_match_production_rule(self):
        result = summarize()
        self.assertAlmostEqual(result["false_fail_probability_one_nominal_scenario"], 0.131716, delta=0.00001)
        self.assertAlmostEqual(result["pass_probability_one_nominal_scenario"], 0.868284, delta=0.00001)
        self.assertAlmostEqual(result["pass_probability_all_scenarios_if_independent"], 0.568390, delta=0.00001)
        self.assertAlmostEqual(result["probability_at_least_one_false_fail_if_scenarios_independent"], 0.431610, delta=0.00001)
        self.assertAlmostEqual(result["exact_binomial_upper_tail_examples"]["60"], 0.086732, delta=0.00001)
        self.assertAlmostEqual(result["exact_binomial_upper_tail_examples"]["73"], 0.001006, delta=0.00001)


if __name__ == "__main__":
    unittest.main()
