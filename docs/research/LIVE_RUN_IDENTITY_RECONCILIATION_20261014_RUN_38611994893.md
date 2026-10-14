# Live Run Identity Reconciliation — Run 38611994893

## Purpose

Record the exact identity and outcome of the GitHub Actions run inspected on 2026-10-14.

This record separates software verification, data-integrity checks, public artifact availability, and scientific claim status. It has no scientific claim-promotion authority.

---

## Run identity

- Repository: "AhmedPeaRL/maximal-one"
- Branch: "main"
- Workflow run ID: "38611994893"
- Workflow URL: https://github.com/AhmedPeaRL/maximal-one/actions/runs/38611994893
- Run commit SHA: "91ee03e9b3ff5dff091eded0147f8d5f5ea2af68"
- Commit URL: https://github.com/AhmedPeaRL/maximal-one/commit/91ee03e9b3ff5dff091eded0147f8d5f5ea2af68

The core-proof job verified that the checked-out repository commit matched the workflow commit identity.

---

## Job outcomes

- "core-proof": success
- "ingest-witness": success
- "external-collision": success
- "compute (18.20.8)": success
- "compute (20.20.0)": success
- "compute (24.11.1)": success
- "build-report": success
- "gate": failure
- "consensus": skipped
- "verify-core": skipped
- "stability-check": skipped
- "sweep-plus": skipped

The final gate failed at "Enforce replication eligibility after evidence collection".

The recorded failure was insufficient independent replication eligibility, with 0 of the required 2 domains eligible.

---

## Secondary monthly data integrity

The "secondary-monthly-integrity-audit" artifact was produced for this run.

Both recorded sources passed the time-integrity checks:

- "hadcet_monthly": 4,404 monthly observations; zero missing or non-finite values; raw and parsed checksums matched the manifest.
- "fred_indpro": 1,284 monthly observations; zero missing or non-finite values; raw and parsed checksums matched the manifest.

Both records remained in the status:

"TIME_INTEGRITY_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW"

The audit does not approve source independence, replication eligibility, stochastic-null adequacy, or claim promotion.

---

## Scientific state

- Scientific claim status: "under_investigation"
- Primary stochastic-null p-value: "0.999001"
- Primary stochastic null rejected: "false"
- Required independent secondary replication domains: 2
- Currently eligible independent secondary domains: 0
- Confirmatory null protocol: not frozen
- Claim promotion authority: false

The permutation-null result is diagnostic-only and does not replace the primary stochastic-null test.

The AR(p) boundary-saturation result is a model-capacity diagnostic. It neither establishes nor falsifies the scientific hypothesis by itself.

No HCM causation, mechanism, consciousness, or universality claim is established by this run.

---

## Public artifact and reproducibility limitation

The workflow logs recorded HTTP 404 responses while attempting to retrieve a public "canonical_report.json" path.

The scientific interpretation also recorded:

- "fingerprint_match": false
- "independent_rerun": "not_verified"

Therefore, public retrieval and independent reproducibility must not be described as established for this run.

The publication path must be repaired and verified against the exact intended report before external verification can be considered complete.

A workflow artifact existing inside GitHub Actions is not, by itself, proof that the same artifact is publicly retrievable from the repository or GitHub Pages.

---

## Relevant artifact identifiers

- "secondary-monthly-integrity-audit": "11917874342"
- "dataset-eligibility-gate": "11917894353"
- "canonical-report": "11920026400"
- "report-hash": "11919441654"
- "external-replay-verification": "11919496468"
- "independent-verification": "11920486320"
- "final-provenance-closure": "11920775954"
- "reproducibility-manifest": "11919821197"

Workflow artifacts are associated with the run above and may be subject to GitHub retention policies.

---

## Required follow-up

1. Preserve the current scientific thresholds, claim status, observed values, and replication requirements.
2. Repair the public canonical-report publication/retrieval path and verify the exact published bytes.
3. Review the AR(p) null family for adequacy using a declared calibration procedure separate from confirmatory evaluation.
4. Freeze the confirmatory protocol prospectively before evaluating fresh confirmation data.
5. Review HadCET and INDPRO source independence and shared nuisance structure.
6. Keep replication eligibility false until the declared evidence requirements are satisfied.
7. Record the exact commit, run ID, job outcomes, artifact IDs, and any remaining failure reasons for the next run.

---

## Interpretation boundary

This run demonstrates successful execution of several computational and data-integrity checks, while the final replication gate remains blocked.

It does not establish the scientific hypothesis, independent scientific replication, HCM causation, or universality.

No threshold, source-eligibility flag, or scientific status should be changed merely to obtain a green workflow result.
