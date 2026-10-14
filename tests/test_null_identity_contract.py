import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis.null_protocol import load_null_protocol


class TestNullIdentityContract(unittest.TestCase):
    def test_null_model_and_protocol_are_distinct(self):
        protocol = load_null_protocol()
        self.assertEqual(protocol["model_id"], "stationary_gaussian_ar_p_aic")
        self.assertEqual(
            protocol["protocol_id"],
            "stationary_gaussian_ar_p_aic_v2_exploratory",
        )
        self.assertNotEqual(protocol["model_id"], protocol["protocol_id"])

    def test_null_identity_fields_are_nonempty_strings(self):
        protocol = load_null_protocol()
        for key in ("model_id", "protocol_id"):
            with self.subTest(key=key):
                self.assertIsInstance(protocol[key], str)
                self.assertTrue(protocol[key].strip())

    def test_generated_null_result_carries_protocol_identity(self):
        import numpy as np
        from analysis.appropriate_stochastic_null import parametric_short_memory_null

        protocol = load_null_protocol()
        rng = np.random.default_rng(42)
        x = np.sin(np.arange(600) / 20.0) + rng.normal(0.0, 0.1, 600)
        result = parametric_short_memory_null(x, 0.5, rng, trials=200)

        self.assertEqual(result["null_model"], protocol["model_id"])
        self.assertEqual(result["null_protocol_id"], protocol["protocol_id"])
        self.assertNotEqual(result["null_model"], result["null_protocol_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
