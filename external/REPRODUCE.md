# External Reproduction Protocol

## Purpose

This protocol defines an independent reproduction of the canonical maximal-one scientific pipeline.

The purpose is not to confirm a claim.

The purpose is to determine whether an independent environment can reproduce the declared computation without relying on the original execution environment.

---

## Independence Requirement

The reproduction must be performed in a clean environment that was not used to generate the canonical result.

The external operator must not modify:

- the canonical dataset,
- the analysis implementation,
- the scientific thresholds,
- the generated result,
- or the expected alpha value.

No post-hoc correction is permitted.

---

## Step 1 — Clone

Clone the repository into a clean directory:

git clone https://github.com/AhmedPeaRL/maximal-one.git
cd maximal-one

Record:

git rev-parse HEAD

---

## Step 2 — Record Environment

Record:

python --version
python -c "import numpy; print('numpy', numpy.__version__)"
python -c "import scipy; print('scipy', scipy.__version__)"
python -c "import platform; print(platform.platform())"

The values must be included in the external reproduction report.

---

## Step 3 — Install Pinned Dependencies

Install exactly the dependencies declared by the repository's locked requirements.

Do not modify the scientific dependency versions.

---

## Step 4 — Run Canonical Pipeline

Run:

python scripts/generate_report.py --seed 42 --canonical

The run must complete without modifying scientific source code.

---

## Step 5 — Verify Canonical Output

Confirm that:

artifacts/canonical_report.json

exists.

Record:

sha256sum artifacts/canonical_report.json

Also record the canonical alpha:

python - <<'PY'
import json

with open(
    "artifacts/canonical_report.json",
    "r",
    encoding="utf-8"
) as f:
    report = json.load(f)

print(
    "canonical_alpha:",
    report["spectral_profile"]["estimated_alpha"]
)
PY

---

## Step 6 — Verify Internal Scientific Consistency

Run:

python scripts/validate_canonical_report.py

A successful execution is required.

---

## Step 7 — Independent Replay Verification

The external operator must compare the reproduced canonical alpha with the canonical reference supplied by the repository.

The comparison must be performed without modifying the reproduced result.

The following fields must be recorded:

- original_alpha
- reproduced_alpha
- delta
- external_report_sha256
- reproduced_report_sha256
- python version
- numpy version
- scipy version
- platform
- repository commit
- verification method

---

## Step 8 — No Silent Substitution

If the reproduction fails because a dataset, estimator, dependency, or validation layer differs, the failure must be reported exactly as observed.

Do not:

- repair the dataset silently,
- replace a failed dataset,
- change thresholds,
- alter the estimator,
- change the frequency band,
- discard an inconvenient result,
- or modify the canonical report.

A failed reproduction is scientific information.

---

## Step 9 — Reproduction Result

The external operator should produce a JSON document with this structure:

{
  "independent_replay_verified": false,
  "fingerprint_match": false,
  "original_alpha": null,
  "reproduced_alpha": null,
  "delta": null,
  "external_report_sha256": "",
  "reproduced_report_sha256": "",
  "external_environment": {
    "python": "",
    "numpy": "",
    "scipy": "",
    "platform": ""
  },
  "repository_commit": "",
  "verification_method": "independent_clean_environment_rerun",
  "notes": ""
}

The external operator must replace the values with the actual observed results.

No value should be copied from the original report merely to satisfy the schema.

---

## Scientific Interpretation

An independent successful replay does not establish:

- consciousness,
- HCM causation,
- universality,
- mechanism,
- metaphysical emergence,
- or any ontological conclusion.

It establishes only that the declared computational result can be independently reproduced under the stated protocol.

Further claims require further evidence.

---

## Integrity Principle

The repository must preserve negative results.

The purpose of this protocol is not to make the hypothesis pass.

The purpose is to make it possible for the hypothesis to fail honestly.
