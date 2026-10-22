from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess


ROOT = Path(__file__).resolve().parents[1]
MATRIX_RELATIVE_PATH = (
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
)
MATRIX_PATH = ROOT / MATRIX_RELATIVE_PATH

MATRIX = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))

if MATRIX.get("protocol") != "HCM_TYPE1_CALIBRATION_V4_CANDIDATE":
    raise RuntimeError("Unexpected Type-I calibration protocol.")

DESIGN = MATRIX.get("candidate_dimensions_not_frozen")
if not isinstance(DESIGN, dict):
    raise RuntimeError(
        "V4 schema error: candidate_dimensions_not_frozen is required."
    )

SCENARIO_ROWS = MATRIX.get("scenarios")
if not isinstance(SCENARIO_ROWS, list) or len(SCENARIO_ROWS) != 9:
    raise RuntimeError(
        "V4 schema error: exactly nine declared scenarios are required."
    )

SCENARIO_ORDER = [row["scenario_id"] for row in SCENARIO_ROWS]
if len(set(SCENARIO_ORDER)) != len(SCENARIO_ORDER):
    raise RuntimeError("V4 schema error: duplicate scenario_id.")

SCENARIOS = {
    row["scenario_id"]: row["phi"]
    for row in SCENARIO_ROWS
}

# These are candidate values for diagnostics and schema checks only.
# Reading a candidate value does not authorize a formal run.
MASTER_SEED = int(DESIGN["master_seed_candidate"])
NOMINAL_ALPHA = float(DESIGN["nominal_alpha"])
DGP_BURN_IN = int(DESIGN["dgp_burn_in"])
REQUIRED_OUTER_REPETITIONS = int(
    DESIGN["outer_repetitions_per_scenario"]
)
REQUIRED_SURROGATES = int(
    DESIGN["surrogates_requested_per_outer_replicate"]
)
REQUIRED_SAMPLE_SIZE = int(DESIGN["sample_size"])
MIN_CONFIRMATORY_REPETITIONS = REQUIRED_OUTER_REPETITIONS

# Deliberately unresolved. Never replace None with 0.075 or another default.
ACCEPTANCE_RULE = DESIGN.get("acceptance_rule")
MAX_ACCEPTABLE_WILSON_UPPER = None

# A candidate matrix is not a frozen protocol or an execution authorization.
# A future implementation must verify separate, attributable freeze and
# authorization records bound to the exact reviewed commit and file hashes.
V4_APPROVED = False


def stable_scenario_key(scenario_id: str) -> int:
    """Stable 32-bit key derived from scenario identity, never list position."""
    if not isinstance(scenario_id, str) or not scenario_id:
        raise ValueError("scenario_id must be a non-empty string.")
    digest = hashlib.sha256(scenario_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def seed_sequence(
    master_seed: int,
    scenario_id: str,
    replicate_index: int,
    stream_id: int,
) -> np.random.SeedSequence:
    """Construct a reproducible seed identity independent of shard order."""
    if not isinstance(scenario_id, str) or not scenario_id:
        raise ValueError("scenario_id must be a non-empty string.")
    if min(master_seed, replicate_index, stream_id) < 0:
        raise ValueError("Seed components must be non-negative integers.")

    return np.random.SeedSequence([
        int(master_seed),
        stable_scenario_key(scenario_id),
        int(replicate_index),
        int(stream_id),
    ])


def replicate_rngs(
    master_seed: int,
    scenario_id: str,
    replicate_index: int,
) -> tuple[np.random.Generator, np.random.Generator]:
    return (
        np.random.default_rng(
            seed_sequence(master_seed, scenario_id, replicate_index, 0)
        ),
        np.random.default_rng(
            seed_sequence(master_seed, scenario_id, replicate_index, 1)
        ),
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


def generate_ar(
    phi: list[float],
    n: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if n < 1:
        raise ValueError("n must be positive.")

    ar = np.asarray(
        [1.0] + [-float(value) for value in phi],
        dtype=float,
    )
    process = ArmaProcess(ar=ar, ma=np.asarray([1.0]))

    if not bool(process.isstationary):
        raise RuntimeError(
            f"Declared synthetic AR coefficients are not stationary: {phi}"
        )

    values = process.generate_sample(
        nsample=n + DGP_BURN_IN,
        burnin=0,
        distrvs=rng.standard_normal,
    )
    return np.asarray(values[DGP_BURN_IN:], dtype=np.float64)


def acceptance_decision(
    *,
    requested: int,
    completed: int,
    invalid: int,
    upper: float | None,
) -> tuple[bool, str]:
    if requested <= 0:
        return False, "BLOCKED_INVALID_REQUESTED_COUNT"

    if completed != requested:
        return False, "INCOMPLETE_NOT_A_PASS"

    if invalid != 0:
        return False, "TYPE1_CALIBRATION_FAILED_INVALID_ATTEMPTS"

    if upper is None or not np.isfinite(float(upper)):
        return False, "TYPE1_CALIBRATION_FAILED_NO_VALID_BOUND"

    # No acceptance rule has been approved. Do not infer one from history.
    if ACCEPTANCE_RULE is None or MAX_ACCEPTABLE_WILSON_UPPER is None:
        return False, "BLOCKED_ACCEPTANCE_RULE_UNRESOLVED"

    if float(upper) > MAX_ACCEPTABLE_WILSON_UPPER:
        return False, "TYPE1_CALIBRATION_FAILED_UPPER_BOUND"

    return True, "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE"
