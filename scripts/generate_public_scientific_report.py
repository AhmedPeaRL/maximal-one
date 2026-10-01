from __future__ import annotations

import argparse
import json
from pathlib import Path


REPORT = Path("artifacts/canonical_report.json")
OUTPUT = Path("public/scientific_report.md")


def fmt(value, digits=6):
    if value is None:
        return "null"
    return f"{float(value):.{digits}f}"


def build(report):
    spectral = report["spectral_profile"]
    null = report["appropriate_stochastic_null"]
    method = report["cross_method_validation"]
    calibration = report.get("estimator_sensitivity_audit", {})

    alpha = spectral["estimated_alpha"]
    sigma = spectral["bootstrap_std"]
    fft_alpha = method["fft_alpha"]
    delta = method["agreement_delta"]

    p_value = null["p_value_mc_add_one"]
    rejected = null["reject_at_0_05"]

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

Current result:

- observed alpha: `{fmt(null["observed_alpha"])}`
- null mean: `{fmt(null["null_mean"])}`
- null standard deviation: `{fmt(null["null_std"])}`
- valid surrogates: `{null["null_samples"]}`
- exceedances: `{null["exceedances"]}`
- Monte Carlo p-value: `{fmt(p_value)}`
- rejection at 0.05: `{str(rejected).lower()}`

### Scientific decision

The primary stochastic null is **not rejected**.

Therefore the current scientific claim is **not established**.

---

## Null Capacity Diagnostic

The surrogate AR-order boundary fraction is:

`{fmt(null["order_selection_diagnostic"]["surrogate_boundary_fraction"])}`

This is a null-model capacity/calibration warning.

It is not evidence for the scientific hypothesis.

Any replacement null protocol must be declared prospectively before
fresh confirmation data are used.

---

## Estimator Sensitivity

The estimator sensitivity audit is diagnostic only.

No favorable estimator configuration may replace the canonical endpoint
after observing the data.

---

## Secondary Diagnostics

The permutation null result and other secondary diagnostics are not
primary claim-promotion evidence.

---

## Independent Real-Domain Replication

A valid alpha measurement is not scientific replication.

Scientific replication requires eligible independent real domains to
reject the same declared primary stochastic null using the same
endpoint, null family, direction, and tail.

That condition is not currently established.

---

## Computational Reproducibility

Clean-checkout replay establishes computational reproducibility of
the declared execution path.

It does not establish scientific replication or truth of the
scientific hypothesis.

---

## HCM Interpretation Boundary

The current canonical result does not establish HCM causation,
consciousness, universality, mechanism, novel physics, predictive
superiority, or market advantage.

---

## Scientific Decision

`CLAIM = NOT ESTABLISHED`

The system must remain capable of producing and preserving a negative
result.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if not REPORT.exists():
        raise SystemExit(
            "Missing artifacts/canonical_report.json"
        )

    report = json.loads(
        REPORT.read_text(encoding="utf-8")
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
