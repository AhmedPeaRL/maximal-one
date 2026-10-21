from __future__ import annotations

import unittest

import numpy as np
from scipy.signal import welch

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.type1_calibration_pilot import (
    SCENARIOS,
    execute_attempt,
)


class Type1ProductionEquivalenceTests(unittest.TestCase):
    """Real-production-path tests; not a formal calibration."""

    def test_endpoint_matches_independent_reference(self):
        rng = np.random.default_rng(20261021)

        for seed in range(20):
            with self.subTest(seed=seed):
                x = np.random.default_rng(seed).normal(size=3328)
                actual = float(estimate_alpha(x))
                expected = self.reference_alpha(x)

                self.assertTrue(np.isfinite(actual))
                self.assertAlmostEqual(actual, expected, places=8)

    @staticmethod
    def reference_alpha(series):
        """Independent transcription of the declared endpoint."""
        x = np.asarray(series, dtype=np.float64)

        if x.ndim != 1 or len(x) < 256:
            return float("nan")
        if not np.all(np.isfinite(x)) or np.std(x) < 1e-8:
            return float("nan")

        x = x - np.mean(x)
        sd = np.std(x)
        if sd < 1e-12:
            return float("nan")
        x = x / sd

        nperseg = min(1024, len(x))
        freqs = np.fft.rfftfreq(nperseg)
        available = int(np.sum((freqs > 0.01) & (freqs < 0.05)))

        if nperseg < 128 or available < 20:
            return float("nan")

        f, psd = welch(
            x,
            nperseg=nperseg,
            noverlap=nperseg // 2,
            nfft=nperseg,
            window="hann",
            detrend="linear",
            scaling="density",
            return_onesided=True,
            axis=-1,
            average="mean",
        )

        mask = (
            (f > 0.01)
            & (f < 0.05)
            & np.isfinite(f)
            & np.isfinite(psd)
            & (psd > 0)
        )
        f = f[mask]
        psd = psd[mask]

        if len(f) < 20:
            return float("nan")

        if not (
            np.all(np.isfinite(np.log(f)))
            and np.all(np.isfinite(np.log(psd)))
        ):
            return float("nan")

        slope = np.polyfit(np.log(f), np.log(psd), 1)[0]
        return float(np.round(-slope, 8))

    def test_real_null_path_is_repeatable_for_same_replicate(self):
        scenario_id = (
            "gaussian_ar2_inband_f_0_02_radius_0_90_n3328"
        )
        scenario = {
            "scenario_id": scenario_id,
            **SCENARIOS[scenario_id],
        }

        # Real endpoint, real statsmodels null, and real RNG path.
        # 200 is the existing minimum allowed by the pilot/null code.
        first = execute_attempt(
            index=0,
            scenario=scenario,
            master_seed=20261021,
            surrogates=200,
            n=3328,
            burn_in=2000,
        )
        second = execute_attempt(
            index=0,
            scenario=scenario,
            master_seed=20261021,
            surrogates=200,
            n=3328,
            burn_in=2000,
        )

        fields = (
            "replicate_index",
            "dgp_seed_identity",
            "null_seed_identity",
            "generated_series_sha256",
            "observed_alpha",
            "requested_surrogates",
            "valid_surrogates",
            "exceedances",
            "p_value_mc_add_one",
            "selected_order",
            "status",
            "reason",
        )

        for field in fields:
            with self.subTest(field=field):
                self.assertEqual(first.get(field), second.get(field))

        self.assertEqual(first["status"], "VALID")
        self.assertEqual(first["requested_surrogates"], 200)
        self.assertEqual(first["valid_surrogates"], 200)
        self.assertIsNotNone(first["exceedances"])
        self.assertAlmostEqual(
            first["p_value_mc_add_one"],
            (first["exceedances"] + 1) / 201,
            places=15,
        )


if __name__ == "__main__":
    unittest.main()
