from __future__ import annotations

import argparse
import json
from pathlib import Path


REPORT = Path("artifacts/canonical_report.json")
SENSITIVITY = Path("artifacts/estimator_sensitivity_audit.json")
OUTPUT = Path("public/scientific_report.md")


def fmt(value, digits=6):
    if value is None:
        return "null"
    return f"{float(value):.{digits}f}"


def load_optional_json(path: Path):
    if not path.exists():
        return {}

    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def build(report):
    spectral = report["spectral_profile"]
    null = report["appropriate_stochastic_null"]
    method = report["cross_method_validation"]

    sensitivity = load_optional_json(
        SENSITIVITY
    )

    alpha = spectral["estimated_alpha"]
    fft_alpha = method["fft_alpha"]
    delta = method["agreement_delta"]

    p_value = null["p_value_mc_add_one"]
    rejected = null["reject_at_0_05"]

    summary = sensitivity.get(
        "summary",
        {}
    )

    minimum_alpha = summary.get(
        "minimum_alpha"
    )

    maximum_alpha = summary.get(
        "maximum_alpha"
    )

    alpha_range = summary.get(
        "alpha_range"
    )

    boundary_fraction = (
        null[
            "order_selection_diagnostic"
        ][
            "surrogate_boundary_fraction"
        ]
    )

    boundary_percent = (
        float(boundary_fraction) * 100.0
    )

    permutation_p = report[
        "statistical_test"
    ][
        "p_value"
    ]

    return f"""# MAXIMAL-ONE — Scientific Status Report

## Current Status

**UNDER INVESTIGATION**

The current canonical validation pipeline does not establish the
Constrained Spectral Persistence Hypothesis.

No scientific claim is promoted by the current evidence.

---

## Current Canonical Measurement

Primary dataset:

`real-data/sunspots_full.csv`

Primary sample size:

`N = {report["dataset_audit"]["primary_length"]}`

Canonical estimator:

`{spectral["alpha_provenance"]["estimator"]}`

Canonical frequency band:

`{spectral["alpha_provenance"]["frequency_band"][0]}–{spectral["alpha_provenance"]["frequency_band"][1]}`

Canonical segmentation:

`nperseg = {spectral["alpha_provenance"]["nperseg"]}`

Canonical spectral exponent:

`alpha = {fmt(alpha)}`

Independent FFT-periodogram estimate:

`alpha = {fmt(fft_alpha)}`

Absolute method difference:

`{fmt(delta)}`

The agreement between Welch and FFT is a measurement-consistency
result. It is not independent scientific replication.

---

## Primary Stochastic Null

The current exploratory primary stochastic null is:

`{null["null_model"]}`

with:

- stationary fitted AR models;
- AIC order selection;
- order range `1..20`;
- Gaussian innovations;
- refitting for each surrogate;
- canonical primary alpha as the endpoint;
- upper-tail alternative.

Current result:

- observed alpha: `{fmt(null["observed_alpha"])}`
- null mean: `{fmt(null["null_mean"])}`
- null standard deviation: `{fmt(null["null_std"])}`
- valid surrogates: `{null["null_samples"]}`
- exceedances: `{null["exceedances"]}`
- Monte Carlo p-value: `{fmt(p_value)}`
- rejection at `0.05`: `{str(rejected).lower()}`

### Scientific decision

The primary stochastic null is **not rejected**.

Therefore the current scientific claim is **not established**.

---

## Null Capacity Diagnostic

The surrogate AR-order boundary fraction is:

`{boundary_percent:.1f}%`

Therefore {boundary_percent:.1f}% of surrogate refits selected the maximum
declared order of `{null["selected_order_max"]}`.

This is treated as a null-model capacity/calibration warning.

It is not evidence for the scientific hypothesis.

The repository must not increase the AR order merely to obtain a more
favorable inferential result.

Any replacement null protocol must be declared prospectively before
fresh confirmation data are used.

---

## Estimator Sensitivity

A prospective estimator sensitivity audit was performed.

Across valid combinations of the declared frequency bands and Welch
segment lengths:

- minimum observed alpha: `{fmt(minimum_alpha)}`
- maximum observed alpha: `{fmt(maximum_alpha)}`
- alpha range: `{fmt(alpha_range)}`

The canonical configuration produces:

`alpha = {fmt(alpha)}`

Several reasonable alternative configurations produce materially
different values.

Therefore the current data do not justify treating `alpha` as a
configuration-independent universal scalar.

The sensitivity audit is diagnostic only.

No favorable estimator configuration may replace the canonical endpoint
after observing the data.

---

## Secondary Diagnostics

The permutation null produced:

`p = {fmt(permutation_p)}`

This result concerns the specified exchangeability/permutation null
only.

It is **diagnostic only** and is not the primary stochastic-null
decision.

Other diagnostic layers include:

- cross-method agreement;
- multi-scale behavior;
- perturbation stability;
- phase-surrogate behavior;
- predictive validation;
- adversarial controls.

None of these independently establishes the scientific claim.

---

## Independent Real-Domain Replication

The repository requires at least two independent real secondary
domains.

A valid alpha measurement is not scientific replication.

Scientific replication requires each eligible independent real domain
to reject the same declared primary stochastic null using:

- the same endpoint;
- the same null family;
- the same direction;
- the same tail;
- the same scientific decision rule.

That condition is not currently established.

---

## Computational Reproducibility

Clean-checkout replay establishes computational reproducibility of the
declared execution path.

It does not establish:

- scientific replication;
- independent implementation replication;
- laboratory replication;
- truth of the scientific hypothesis.

---

## HCM Interpretation Boundary

The current canonical spectral result does not establish:

- HCM causation;
- consciousness;
- a physical field;
- universality;
- novel physics;
- predictive superiority;
- market advantage;
- mechanism.

HCM-related interpretations remain conceptual hypotheses outside the
current empirical claim authority.

---

## Scientific Decision

The current machine-gated decision is:

`CLAIM = NOT ESTABLISHED`

This is an intended scientific outcome.

The system must remain capable of producing and preserving a negative
result.

---

## Next Scientific Phase

The next phase is methodological:

1. complete null-model calibration and adequacy analysis;
2. formally predeclare the future primary null;
3. freeze the future confirmation protocol;
4. analyze fresh confirmation data;
5. require independent real-domain replication;
6. require clean-checkout computational reproducibility;
7. preserve all failed outcomes.

No threshold, endpoint, tail, estimator, or null family should be
changed solely to obtain a favorable result.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true"
    )

    args = parser.parse_args()

    if not REPORT.exists():
        raise SystemExit(
            "Missing artifacts/canonical_report.json"
        )

    report = json.loads(
        REPORT.read_text(
            encoding="utf-8"
        )
    )

    generated = build(report)

    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(
                "public/scientific_report.md is missing"
            )

        current = OUTPUT.read_text(
            encoding="utf-8"
        )

        if current != generated:
            raise SystemExit(
                "public/scientific_report.md is stale. "
                "Regenerate it from canonical_report.json."
            )

        print(
            "Scientific public report matches canonical report."
        )
        return

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        generated,
        encoding="utf-8"
    )

    print(
        f"Wrote {OUTPUT}"
    )


if __name__ == "__main__":
    main()
