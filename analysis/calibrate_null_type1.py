from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess

MATRIX_PATH = Path("protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json")
MATRIX = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
PRIMARY = MATRIX["primary_design"]
SCENARIO_ROWS = MATRIX["scenarios"]
SCENARIO_ORDER = [row["scenario_id"] for row in SCENARIO_ROWS]
SCENARIOS = {row["scenario_id"]: row["phi"] for row in SCENARIO_ROWS}
MASTER_SEED = int(PRIMARY["seed_schedule"]["master_seed"])
NOMINAL_ALPHA = float(PRIMARY["nominal_alpha"])
MAX_ACCEPTABLE_WILSON_UPPER = float(PRIMARY["one_sided_upper_bound_maximum"])
REQUIRED_OUTER_REPETITIONS = int(PRIMARY["outer_repetitions_per_scenario"])
REQUIRED_SURROGATES = int(PRIMARY["surrogates_requested_per_outer_replicate"])
REQUIRED_SAMPLE_SIZE = int(PRIMARY["sample_size"])
MIN_CONFIRMATORY_REPETITIONS = REQUIRED_OUTER_REPETITIONS


def seed_sequence(master_seed: int, scenario_index: int, replicate_index: int, stream_id: int) -> np.random.SeedSequence:
    """Stable independent seed identity; independent of execution/shard order."""
    if min(master_seed, scenario_index, replicate_index, stream_id) < 0:
        raise ValueError("SeedSequence components must be non-negative integers")
    return np.random.SeedSequence([int(master_seed), int(scenario_index), int(replicate_index), int(stream_id)])


def replicate_rngs(master_seed: int, scenario_index: int, replicate_index: int) -> tuple[np.random.Generator, np.random.Generator]:
    return (
        np.random.default_rng(seed_sequence(master_seed, scenario_index, replicate_index, 0)),
        np.random.default_rng(seed_sequence(master_seed, scenario_index, replicate_index, 1)),
    )


def wilson_interval(successes: int, trials: int, confidence: float = 0.95) -> tuple[float, float]:
    """Two-sided Wilson score interval, reported for context only."""
    if trials <= 0 or successes < 0 or successes > trials:
        return (float("nan"), float("nan"))
    from scipy.stats import norm
    z = float(norm.ppf(0.5 + confidence / 2.0))
    p = successes / trials
    denom = 1.0 + z * z / trials
    center = (p + z * z / (2.0 * trials)) / denom
    half = z * np.sqrt((p * (1.0 - p) / trials) + (z * z / (4.0 * trials * trials))) / denom
    return max(0.0, float(center - half)), min(1.0, float(center + half))


def wilson_upper_one_sided(successes: int, trials: int, confidence: float = 0.95) -> float:
    """One-sided Wilson upper confidence bound used by V3 candidate rule."""
    if trials <= 0 or successes < 0 or successes > trials:
        return float("nan")
    from scipy.stats import norm
    z = float(norm.ppf(confidence))
    p = successes / trials
    denom = 1.0 + z * z / trials
    center = p + z * z / (2.0 * trials)
    half = z * np.sqrt((p * (1.0 - p) / trials) + (z * z / (4.0 * trials * trials)))
    return min(1.0, float((center + half) / denom))


def generate_ar(phi: list[float], n: int, rng: np.random.Generator) -> np.ndarray:
    ar = np.asarray([1.0] + [-float(value) for value in phi], dtype=float)
    process = ArmaProcess(ar=ar, ma=np.asarray([1.0]))
    if not bool(process.isstationary):
        raise RuntimeError(f"Declared synthetic AR coefficients are not stationary: {phi}")
    values = process.generate_sample(nsample=n + int(PRIMARY["dgp_burn_in"]), burnin=0, distrvs=rng.standard_normal)
    return np.asarray(values[int(PRIMARY["dgp_burn_in"]):], dtype=np.float64)


def acceptance_decision(*, requested: int, completed: int, invalid: int, upper: float | None) -> tuple[bool, str]:
    if completed != requested:
        return False, "INCOMPLETE_NOT_A_PASS"
    if invalid != 0:
        return False, "TYPE1_CALIBRATION_FAILED_INVALID_ATTEMPTS"
    if upper is None or not np.isfinite(float(upper)):
        return False, "TYPE1_CALIBRATION_FAILED_NO_VALID_BOUND"
    if float(upper) > MAX_ACCEPTABLE_WILSON_UPPER:
        return False, "TYPE1_CALIBRATION_FAILED_UPPER_BOUND"
    return True, "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE"
