# Independent Human Statistical Review — Exact Snapshot

Status: REVIEW HANDOFF ONLY — NOT AN APPROVAL

Protocol freeze: NOT_FROZEN
Formal calibration: NOT_AUTHORIZED
Confirmatory execution: NOT_AUTHORIZED
Claim support: false
Promotion authority: false

## 1. Exact review snapshot

Repository: AhmedPeaRL/maximal-one

Branch: review/type1-v4-remediation

Exact commit:
e8e127259e475b06599d3f5fc550cd6a616a127f

Inventory run: 41349619676
Inventory job: 124976784699
Inventory artifact: 13100800974

Snapshot run: 41349751627
Snapshot job: 124977174577
Snapshot artifact: 13099834438

Snapshot ZIP SHA-256:
440529730ba5111baef36abf4429b3de8dd41f24cf4c11b170f1ee4d0ce57c5f

Manifest SHA-256:
7b7aa0d1409048779ee324a80a69b37d755c9539d23beb5d6fbac16585695a16

SHA256SUMS SHA-256:
71e9f6a60bed0b0e3f92d594d446bcc0b68a46a1cd0c70f37e98d788c1c72528

The snapshot ZIP contains a manifest and checksums,
not the source files themselves. Review the exact Git commit
or provide a separately verified source bundle.

## 2. Exact protocol input hashes

V4 candidate matrix:
f8b8dfaf97282ca24378b8929939d8fffd1fe72064a2fe662198422a11b1bc2f

V4 draft matrix:
b6c6354558ca6a0685f5731da11da656268c1c3e44599f84f5540ad9725f11af

Independent review request:
26f62a6f47488c1d55dea4cd0548d8f0cf43578bbeea8fb9669ee4ec45e087f7

Formal runner:
faf96a9e969f1060d51142503521e2857ff0b4c11cfa53fbe4fab6f0c318b86a

Scenario runner:
84cda5c6674b5f692cca1e64bd153390db30804f9d21984547ccce57d2c996ff

## 3. Candidate design

The V4 candidate declares nine stationary Gaussian AR
scenarios, including two in-band resonant AR(2) scenarios.

Candidate dimensions:
- 2,000 outer repetitions per scenario.
- 1,000 requested surrogate fits per outer repetition.
- Sample size 3,328.
- DGP burn-in 2,000.
- Nominal alpha 0.05.
- Candidate master seed 20261021.
- Invalid attempts are preserved and block a pass.
- Missing attempts cannot be silently dropped.
- Acceptance rule remains unresolved.
- The 0.075 ceiling is not approved.

The V4 candidate is not a frozen protocol.

## 4. Required statistical decisions

The reviewer must explicitly assess:

A. The exact Type-I error estimand and rejection event.

B. Whether the correct acceptance rule is:
- historical two-sided 95% Wilson interval;
- one-sided 95% Wilson upper bound;
- or another prospectively justified rule.

C. Whether the 0.075 ceiling is justified.

D. How multiplicity across nine scenarios is handled.

E. Whether every scenario must pass.

F. Whether 2,000 outer repetitions provide adequate Monte Carlo
precision, and whether 1,000 surrogates per attempt are justified.

G. Whether sample size 3,328 and burn-in 2,000 are appropriate.

H. Whether all nine scenarios are stationary and correctly
parameterized, including the two resonant AR(2) cases.

I. Whether the calibration runner is equivalent to the actual
production endpoint and null procedure.

J. How invalid attempts, missing artifacts, failed fits,
and surrogate shortfalls affect the denominator and decision.

Historical V1 results remain NOT_PASSED under the historical
two-sided rule. No historical result may be reclassified
to make a later candidate pass.

## 5. Reviewer attribution and conflicts

Reviewer full name: [REQUIRED]
Professional affiliation: [REQUIRED]
Relevant statistical qualifications: [REQUIRED]
Relevant methodological publications: [REQUIRED]
Experience with time series and Monte Carlo calibration: [REQUIRED]
Prior involvement with the project: [REQUIRED — state NONE]
Financial or professional conflicts: [REQUIRED — state NONE]
Review date: [REQUIRED]
Attributable written confirmation or signature: [REQUIRED]

AI-generated analysis is not an independent human review.

## 6. Required disposition

Select exactly one:

APPROVE_WITH_EXPLICIT_RATIONALE
REVISE_AND_RESUBMIT
REJECT
INSUFFICIENT_INFORMATION

The reviewer must provide:
- exact reviewed commit and file hashes;
- explicit decision on Wilson sidedness and threshold;
- scenario and parameterization findings;
- sample-size and repetition-count rationale;
- multiplicity and invalid-attempt policy;
- implementation-equivalence findings;
- limitations and required amendments;
- explicit statement whether the protocol is ready to freeze.

## 7. Non-authorization

This request does not authorize protocol freeze,
formal Type-I calibration, power analysis, claim support,
or promotion authority.

Any later freeze and execution authorization must be
separate, attributable, prospective, and bound to exact
commit and file hashes.
