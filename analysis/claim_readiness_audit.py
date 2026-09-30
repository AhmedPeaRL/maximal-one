from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import periodogram
from statsmodels.stats.diagnostic import acorr_ljungbox

from analysis.load_real_datasets import DATASETS, load_series
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.appropriate_stochastic_null import _stationary_fit

OUTPUT = Path(
    "artifacts/claim_readiness_audit.json"
)

PRIMARY_PATH = Path(
    "real-data/sunspots_full.csv"
)

SEED = 42

ORDER_SCAN_MAX = 40
LJUNG_BOX_LAGS = [10, 20, 40]

def finite(value):
    return (
        isinstance(value, (int, float, np.number))
        and np.isfinite(float(value))
    )

def safe_float(value):
    if finite(value):
        return float(value)
    return None

def load_primary():
    df = pd.read_csv(
        PRIMARY_PATH,
        sep=";",
        header=None,
        engine="python",
        on_bad_lines="skip",
    )

    if df.shape[1] < 4:
        raise ValueError(
            "sunspots_full.csv has fewer than 4 columns"
        )

    series = pd.to_numeric(
        df.iloc[:, 3],
        errors="coerce",
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(series) < 256:
        raise ValueError(
            "primary series is too short"
        )

    if not np.all(np.isfinite(series)):
        raise ValueError(
            "primary series contains non-finite values"
        )

    return series

def alpha_summary(series):
    full_alpha = estimate_alpha(series)

    half = series[: len(series) // 2]
    half_alpha = estimate_alpha(half)

    delta = (
        abs(float(full_alpha) - float(half_alpha))
        if (
            np.isfinite(full_alpha)
            and np.isfinite(half_alpha)
        )
        else np.nan
    )

    return {
        "full_alpha": safe_float(full_alpha),
        "half_alpha": safe_float(half_alpha),
        "half_full_delta": safe_float(delta),
    }

def order_scan(series):
    results = []

    max_order = min(
        ORDER_SCAN_MAX,
        max(1, len(series) // 10),
    )

    for order in range(1, max_order + 1):
        try:
            fit = (
                __import__(
                    "statsmodels.tsa.ar_model",
                    fromlist=["AutoReg"],
                )
                .AutoReg(
                    series,
                    lags=order,
                    trend="c",
                    old_names=False,
                )
                .fit()
            )

            roots = np.asarray(
                fit.roots,
                dtype=np.complex128,
            )

            stationary = bool(
                roots.size == order
                and np.all(np.abs(roots) > 1.0)
            )

            results.append(
                {
                    "order": order,
                    "aic": safe_float(fit.aic),
                    "bic": safe_float(fit.bic),
                    "stationary": stationary,
                }
            )

        except Exception as exc:
            results.append(
                {
                    "order": order,
                    "aic": None,
                    "bic": None,
                    "stationary": False,
                    "error": str(exc),
                }
            )

    valid = [
        item
        for item in results
        if (
            item.get("stationary") is True
            and finite(item.get("aic"))
        )
    ]

    if not valid:
        raise RuntimeError(
            "No stationary AR order was successfully fitted"
        )

    best = min(
        valid,
        key=lambda item: item["aic"],
    )

    return {
        "scan_max_order": max_order,
        "best_aic_order": best["order"],
        "best_aic": best["aic"],
        "best_at_scan_boundary": (
            best["order"] == max_order
        ),
        "results": results,
    }

def residual_diagnostics(series, order):
    from statsmodels.tsa.ar_model import AutoReg

    fit = AutoReg(
        series,
        lags=int(order),
        trend="c",
        old_names=False,
    ).fit()

    residuals = np.asarray(
        fit.resid,
        dtype=np.float64,
    )

    lb = acorr_ljungbox(
        residuals,
        lags=LJUNG_BOX_LAGS,
        return_df=True,
    )

    ljung_box = {}

    for lag in LJUNG_BOX_LAGS:
        row = lb.loc[lag]

        ljung_box[str(lag)] = {
            "statistic": safe_float(
                row["lb_stat"]
            ),
            "p_value": safe_float(
                row["lb_pvalue"]
            ),
        }

    return {
        "residual_count": int(len(residuals)),
        "residual_std": safe_float(
            np.std(residuals)
        ),
        "ljung_box": ljung_box,
    }

def spectral_peak_diagnostic(series):
    x = np.asarray(
        series,
        dtype=np.float64,
    )

    x = x - np.mean(x)

    std = np.std(x)

    if std <= 1e-12:
        return {
            "valid": False,
            "reason": "degenerate_series",
        }

    x = x / std

    freqs, psd = periodogram(
        x,
        detrend="linear",
        scaling="density",
    )

    mask = (
        (freqs > 0.0)
        & np.isfinite(freqs)
        & np.isfinite(psd)
        & (psd > 0)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) == 0:
        return {
            "valid": False,
            "reason": "empty_periodogram",
        }

    peak_index = int(
        np.argmax(psd)
    )

    total_power = float(
        np.sum(psd)
    )

    peak_power = float(
        psd[peak_index]
    )

    return {
        "valid": True,
        "peak_frequency": safe_float(
            freqs[peak_index]
        ),
        "peak_period_samples": safe_float(
            1.0 / freqs[peak_index]
        ),
        "peak_power_fraction": safe_float(
            peak_power / total_power
            if total_power > 0
            else np.nan
        ),
    }

def domain_eligibility_audit():
    results = []

    for name, path in DATASETS.items():

        entry = {
            "name": name,
            "path": path,
            "independent_real_candidate": (
                name in {
                    "co2",
                    "passengers",
                    "cosmic_rays",
                    "temperature",
                    "sp500",
                }
            ),
        }

        try:
            series = load_series(path)

            alpha = estimate_alpha(series)

            entry.update(
                {
                    "load_status": "success",
                    "rows": int(len(series)),
                    "alpha": safe_float(alpha),
                    "estimator_valid": bool(
                        np.isfinite(alpha)
                    ),
                    "eligible_for_alpha_replication": bool(
                        np.isfinite(alpha)
                        and len(series) >= 256
                    ),
                }
            )

        except Exception as exc:
            entry.update(
                {
                    "load_status": "failure",
                    "rows": None,
                    "alpha": None,
                    "estimator_valid": False,
                    "eligible_for_alpha_replication": False,
                    "error": str(exc),
                }
            )

        results.append(entry)

    return results

def main():
    primary = load_primary()

    alpha = alpha_summary(
        primary
    )

    scan = order_scan(
        primary
    )

    best_order = int(
        scan["best_aic_order"]
    )

    residuals = residual_diagnostics(
        primary,
        best_order,
    )

    peak = spectral_peak_diagnostic(
        primary
    )

    domains = domain_eligibility_audit()

    null_calibration_path = Path(
        "artifacts/null_calibration_gate.json"
    )

    replication_gate_path = Path(
        "artifacts/independent_domain_replication_gate.json"
    )

    replay_path = Path(
        "artifacts/external_replay_verification.json"
    )

    null_calibration = (
        json.loads(
            null_calibration_path.read_text(
                encoding="utf-8"
            )
        )
        if null_calibration_path.exists()
        else None
    )

    replication_gate = (
        json.loads(
            replication_gate_path.read_text(
                encoding="utf-8"
            )
        )
        if replication_gate_path.exists()
        else None
    )

    replay = (
        json.loads(
            replay_path.read_text(
                encoding="utf-8"
            )
        )
        if replay_path.exists()
        else None
    )
    
    primary_report = {
        "valid": False,
        "support_eligible": False,
        "rejected": False,
    }

    canonical_report_path = Path(
        "artifacts/canonical_report.json"
    )

    if canonical_report_path.exists():
        try:
            canonical_report = json.loads(
                canonical_report_path.read_text(
                    encoding="utf-8"
                )
            )

            primary_null = canonical_report.get(
                "appropriate_stochastic_null",
                {}
            )

            primary_report = {
                "valid": (
                    primary_null.get("valid") is True
                ),
                "support_eligible": (
                    primary_null.get(
                        "support_eligible"
                    ) is True
                ),
                "rejected": (
                    primary_null.get(
                        "reject_at_0_05"
                    ) is True
                ),
            }

        except Exception:
            primary_report = {
                "valid": False,
                "support_eligible": False,
                "rejected": False,
            }

    primary_null_calibrated = (
        null_calibration is not None
        and null_calibration.get(
            "status"
        ) == "CALIBRATION_NOT_REJECTED"
    )

    independent_domain_replication_established = (
        replication_gate is not None
        and replication_gate.get(
            "status"
        ) == "REPLICATION_ESTABLISHED"
    )

    computational_reproducibility_verified = (
        replay is not None
        and replay.get(
            "computational_reproducibility_verified"
        ) is True
        and replay.get(
            "fingerprint_match"
        ) is True
        and replay.get(
            "structure_match"
        ) is True
    )

    scientific_replication_verified = (
        independent_domain_replication_established
    )

    promotion_allowed = bool(
        primary_report["rejected"]
        and primary_null_calibrated
        and independent_domain_replication_established
        and computational_reproducibility_verified
    )

    claim_readiness = {
        "scientific_claim_supported": bool(
            promotion_allowed
        ),

        "primary_stochastic_null_rejected": bool(
            primary_report["rejected"]
        ),

        "primary_stochastic_null_valid": bool(
            primary_report["valid"]
        ),

        "primary_stochastic_null_support_eligible": bool(
            primary_report["support_eligible"]
        ),

        "primary_null_calibrated": bool(
            primary_null_calibrated
        ),

        "independent_domain_replication_established": bool(
            independent_domain_replication_established
        ),

        "computational_reproducibility_verified": bool(
            computational_reproducibility_verified
        ),

        "scientific_replication_verified": bool(
            scientific_replication_verified
        ),

        "promotion_allowed": bool(
            promotion_allowed
        ),
    }

    report = {
        "status": "diagnostic_only",
        "scientific_claim_authority": False,
        "claim_readiness": claim_readiness,
        "seed": SEED,

        "primary": {
            "path": str(PRIMARY_PATH),
            "rows": int(len(primary)),
            "alpha": alpha,
        },

        "ar_order_scan": scan,

        "selected_order_residual_diagnostics": residuals,

        "spectral_peak_diagnostic": peak,

        "domain_eligibility": domains,

        "interpretation": {
            "promotion_decision": (
                "This audit does not promote or reject "
                "the scientific claim."
            ),
            "order_boundary": (
                "If the best stationary AIC order reaches "
                "the scan boundary, the declared short-memory "
                "null requires further calibration before "
                "stronger inference."
            ),
            "temporal_instability": (
                "A large half/full alpha difference is retained "
                "as a stability warning and is never corrected "
                "automatically."
            ),
            "periodicity": (
                "Peak diagnostics are descriptive only and do "
                "not establish or refute a persistence mechanism."
            ),
        },
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "=== CLAIM READINESS AUDIT ==="
    )

    print(
        "Primary alpha:",
        alpha["full_alpha"],
    )

    print(
        "Half alpha:",
        alpha["half_alpha"],
    )

    print(
        "Half/full delta:",
        alpha["half_full_delta"],
    )

    print(
        "Best AIC order:",
        scan["best_aic_order"],
    )

    print(
        "Best order at scan boundary:",
        scan["best_at_scan_boundary"],
    )

    print(
        "Spectral peak:",
        peak,
    )

    print(
        f"Saved: {OUTPUT}"
    )

if __name__ == "__main__":
    main()
