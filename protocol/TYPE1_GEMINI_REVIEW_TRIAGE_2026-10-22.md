# Type-I V4 — Gemini Review Report Triage

- **Date:** 2026-10-22
- **Repository:** `AhmedPeaRL/maximal-one`
- **Working branch:** `review/type1-v4-remediation`
- **Protocol:** `HCM_TYPE1_CALIBRATION_V4_DRAFT`
- **Disposition:** `USEFUL_SUPPORTING_ANALYSIS; INDEPENDENT_REVIEW_GATE_NOT_CLOSED`

## 1. Purpose and limits

This record evaluates the Gemini-assisted review text submitted on 2026-10-22. It records useful methodological observations and compares them with the current V4 draft and inspected GitHub Actions evidence.

This record is not an attributable independent human statistical approval, protocol freeze, formal-calibration authorization, calibration result, or evidence supporting the broader HCM research claim.

The submitted text's description of itself as a human independent review is not sufficient to establish reviewer identity, expertise, independence, or attributable approval. Those facts must be documented by the actual reviewer and must not be inferred.

## 2. Repository and execution evidence inspected

### E1 — Full-path engineering equivalence test

* Commit: `f8b7614cca394320c59501d5f09517ba57e5e44a`
* Workflow run: `39672639916`
* Job: `119474224176`
* Result: `success`
* Test: `tests.test_type1_full_path_equivalence.Type1FullPathEquivalenceTests.test_real_runner_merger_reverse_merge_and_resume`
* Artifact ID: `12380223302`
* Artifact name: `type1-full-path-equivalence-evidence`
* Artifact ZIP SHA-256: `88f7576c0cef5073f935ed5175ca23f78f6a98af2bbff1d6c7fb3534a9d1a11c`
* Artifact URL: `https://github.com/AhmedPeaRL/maximal-one/actions/runs/39672639916/artifacts/12380223302`

The recorded test exercised a fresh connected run, separate real runner shards, normal-order merge, reverse-order merge, verified checkpoint resume, and rejection of a corrupted shard.

The test used two outer replicate indices and 200 surrogates per attempt. This is engineering-equivalence evidence for the tested configuration only. It does not establish formal Type-I calibration or production equivalence at 1,000 surrogates.

### E2 — Exploratory runtime pilot

* Commit: `413ea997cf8a57707109921880c6e53dbafd081b`
* Workflow run: `39646209338`
* Job: `119382352479`
* Result: `success`
* Artifact ID: `12367063083`
* Artifact ZIP SHA-256: `456c3427d1e0c9452717a5730d1ad4bc535d28e0cc3d273ef8cec5cc13d92522`
* Artifact URL: `https://github.com/AhmedPeaRL/maximal-one/actions/runs/39646209338/artifacts/12367063083`

The inspected logs show eight pilot tests and two production-equivalence tests passing, followed by an exploratory run with two outer repetitions and 200 surrogates per attempt. This remains diagnostic-only evidence.

Artifact ZIP digests identify the uploaded ZIP objects; they are not hashes of individual JSON payloads.

## 3. Disposition of the submitted methodological recommendations

### 3.1 Endpoint and Type-I estimand

**Disposition:** `REVISE_AND_REVIEW_AGAIN`

The report describes the endpoint generically. It does not provide a complete, independently reasoned assessment of the exact `canonical_primary_alpha` implementation, invalid-input rules, spectral settings, rounding, and failure semantics.

The protocol must distinguish:

* Outer repetitions, which estimate the rejection probability of the complete test under each declared null DGP.
* Inner surrogate draws, which are used to calculate the Monte Carlo p-value for each outer test.

The empirical Type-I estimate for a scenario is based on outer test outcomes, not on the inner surrogate count alone.

### 3.2 Null-model scope

**Disposition:** `REVISE_AND_REVIEW_AGAIN`

The current V4 draft proposes stationary Gaussian AR(p) surrogate fitting, AIC selection over candidate orders 1–20, a constant trend, stationarity checks, and a specified hold-back.

The report's examples of AR(1) through AR(10), block shuffling, and spectral surrogates do not constitute approval to add or substitute those procedures. Any added null family requires a prospective rationale, explicit implementation specification, and review before confirmatory outcomes are inspected.

### 3.3 Sample size and burn-in

**Disposition:** `BLOCKED_PENDING_ATTRIBUTABLE_REVIEW`

The V3 candidate specifies sample size 1,024 and burn-in 2,000. The V4 draft matrix specifies sample size 3,328 and burn-in 2,000.

The report's general recommendation of sample sizes between 1,000 and 5,000 and burn-in percentages does not resolve this discrepancy. The final choice requires an explicit prospective rationale tied to the data-generating process and the intended operating-characteristic assessment. Any sensitivity analysis must be planned and documented without using confirmatory outcomes to select a favorable setting.

### 3.4 Surrogate count and Monte Carlo precision

**Disposition:** `BLOCKED_PENDING_ATTRIBUTABLE_REVIEW`

The pilot uses 200 surrogates per outer attempt. The V4 production candidate requests 1,000.

The recommendation of 2,000–5,000 surrogates per test is not adopted automatically. The reviewer must justify the requested count, minimum valid count, p-value resolution, computational feasibility, and the required precision for the intended decision. Outer repetition count and inner surrogate count must be specified separately.

### 3.5 Type-I acceptance criterion

**Disposition:** `BLOCKED_PENDING_ATTRIBUTABLE_REVIEW`

The historical rule requiring a one-sided 95% Wilson upper confidence bound no greater than 0.075 remains unapproved.

The review must justify the relationship between nominal alpha 0.05 and the proposed 0.075 acceptance boundary, the number of outer repetitions, Monte Carlo uncertainty, scenario-specific decisions, invalid attempts, and any multiplicity interpretation.

No threshold may be altered after confirmatory outcomes are inspected merely to obtain a pass.

### 3.6 Invalid attempts and incomplete evidence

**Disposition:** `ACCEPT AS A GOVERNANCE PRINCIPLE; FORMAL POLICY STILL REQUIRES APPROVAL`

The following principle is adopted: invalid attempts, failed fits, surrogate shortfalls, corrupted artifacts, missing records, and interrupted jobs must be recorded and must not be silently dropped, replaced, or counted as non-rejections.

Before freeze, the protocol must specify the exact status and decision consequences for each failure type, whether any retry is permitted, how retries retain original records, and what evidence is required for a complete run.

### 3.7 Full-path equivalence

**Disposition:** `ENGINEERING EVIDENCE OBSERVED; SCIENTIFIC GATE REMAINS OPEN`

Run `39672639916` passed the inspected full-path equivalence test for its tested configuration. The evidence includes real runner execution, sharding, both merge orders, checkpoint resume, and corrupted-shard rejection.

The test's small configuration does not establish that the intended production configuration of 1,000 surrogates has been validated end-to-end. The acceptance ledger must state the exact tested configuration and retain the artifact identity and digest.

### 3.8 Version fingerprints and freeze

**Disposition:** `NOT APPROVED`

The presence of `SYSTEM_STATE_MANIFEST.json`, a release identity, a public-key file, or a historical digest does not by itself identify and freeze the complete V4 protocol and implementation snapshot.

A V4 freeze requires a specific reviewed commit, SHA-256 hashes of every in-scope protocol and implementation file, a documented independent review, closed critical conditions, and a distinct approved freeze decision. Any integrity mechanism must be verified against the exact files it is intended to protect.

## 4. Required discrepancy register

The following issues remain open:

1. Reconcile V3 sample size 1,024 with V4 sample size 3,328.
2. Approve the scientific rationale for burn-in 2,000 under the selected DGPs.
3. Distinguish 200-surrogate pilot execution from the 1,000-surrogate production candidate.
4. Justify the one-sided 95% Wilson upper-bound rule and the historical 0.075 ceiling.
5. Specify the number of outer repetitions and the intended precision of scenario-specific Type-I estimates.
6. Approve the exact null family, candidate order range, model selection, stationarity checks, and surrogate-generation rules.
7. Finalize the invalid-attempt, failed-fit, shortfall, retry, and missing-artifact policy.
8. Complete attributable independent human statistical review against `protocol/TYPE1_INDEPENDENT_REVIEW_BRIEF_V1.md`.
9. Inspect the retained full-path artifact and determine whether additional production-configuration equivalence testing is required.
10. Freeze an exact hash-identified protocol snapshot only after the preceding conditions are satisfied.

## 5. Current gate decision

* Supporting analysis: `RECORDED`
* Engineering full-path test for the observed configuration: `PASS`
* Production-configuration equivalence at 1,000 surrogates: `NOT ESTABLISHED BY THIS TEST`
* Independent human statistical review: `NOT CLOSED`
* V4 freeze: `NOT FROZEN`
* Formal calibration: `NOT AUTHORIZED`
* `confirmatory_execution_authorized`: `false`
* `claim_support`: `false`
* `promotion_authority`: `false`

This record is a prospective governance and evidence-triage document. It does not report formal calibration outcomes and does not authorize execution.
