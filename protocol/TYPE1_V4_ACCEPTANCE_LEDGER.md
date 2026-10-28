# Type-I Calibration V4 — Acceptance Ledger

## 1. Identity and authority

- Protocol: HCM_TYPE1_CALIBRATION_V4_DRAFT
- Working branch: review/type1-v4-remediation
- Current protocol state: DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW
- Freeze state: NOT_FROZEN
- Confirmatory execution authorized: false
- Claim support: false
- Promotion authority: false
- Formal calibration status: NOT AUTHORIZED

This ledger records evidence and unresolved acceptance criteria.
A successful software test is not scientific calibration approval.

## 2. Engineering evidence

### E1 — Locked environment and checkout identity

Status: PASS FOR THE RECORDED WORKFLOW RUN

Evidence:
- Workflow run: 39651504236
- Job: 119400724772
- Tested commit: 060fed17d4646602c5aa5c4b53f2538e25a1b89e
- Python: 3.11.15
- Dependency installation used requirements-lock.txt with hash checking.
- The workflow verified that the checked-out HEAD matched GITHUB_SHA.

Scope:
This verifies the recorded workflow environment and checkout identity.
It does not validate the statistical assumptions.

### E2 — Real runner, merger, reverse merge, and checkpoint resume

Status: PASS FOR THE RECORDED ENGINEERING TEST

Evidence:
- Test: tests/test_type1_full_path_equivalence.py
- Workflow: 39651504236
- Job: 119400724772
- Artifact ID: 12368823752
- Artifact: type1-full-path-equivalence-evidence
- ZIP SHA-256:
  62031070ffe89fd3f89f8de2fe8e0c1601234c452a731d7848f47bf46bc0fd44

The workflow reports successful completion of the real full-path test.
The test exercises the connected runner, separately executed shards,
normal and reverse merge, verified checkpoint resume, and rejection
of a corrupted shard.

Scope:
This is engineering and reproducibility evidence only.
The pilot uses two outer repetitions and 200 surrogates per attempt.
It is not formal Type-I calibration and does not establish the research claim.

### E3 — Updated full-path engineering test, 2026-10-22

**Status:** PASS FOR THE RECORDED TEST CONFIGURATION ONLY

* Commit: `f8b7614cca394320c59501d5f09517ba57e5e44a`
* Workflow run: `39672639916`
* Job: `119474224176`
* Test: `tests.test_type1_full_path_equivalence.Type1FullPathEquivalenceTests.test_real_runner_merger_reverse_merge_and_resume`
* Artifact ID: `12380223302`
* Artifact URL: `https://github.com/AhmedPeaRL/maximal-one/actions/runs/39672639916/artifacts/12380223302`
* Artifact ZIP SHA-256: `88f7576c0cef5073f935ed5175ca23f78f6a98af2bbff1d6c7fb3534a9d1a11c`
* Tested configuration: 2 outer replicate indices and 200 surrogates per attempt.

The inspected job log reports that the real full-path equivalence test passed. The test covers a connected run, separate shards, normal-order merge, reverse-order merge, verified checkpoint resume, and rejection of a corrupted shard.

**Scope limitation:** This establishes successful execution of the recorded engineering test only. It does not establish formal Type-I calibration, production-configuration equivalence at 1,000 surrogates, adequacy of the confirmatory null, or support for the broader research claim. The artifact ZIP digest is not a payload JSON hash.

### E4 — Updated exploratory runtime pilot

**Status:** PASS FOR THE RECORDED DIAGNOSTIC RUN ONLY

* Commit: `413ea997cf8a57707109921880c6e53dbafd081b`
* Workflow run: `39646209338`
* Job: `119382352479`
* Artifact ID: `12367063083`
* Artifact URL: `https://github.com/AhmedPeaRL/maximal-one/actions/runs/39646209338/artifacts/12367063083`
* Artifact ZIP SHA-256: `456c3427d1e0c9452717a5730d1ad4bc535d28e0cc3d273ef8cec5cc13d92522`
* Tested configuration: one exploratory scenario, 2 outer repetitions, and 200 surrogates per attempt.

The inspected job log reports eight pilot tests and two production-equivalence tests passing, followed by successful completion of the small exploratory runtime pilot.

**Scope limitation:** This is diagnostic and engineering evidence, not formal Type-I calibration. It does not authorize the 1,000-surrogate production run or close the independent statistical review gate.

### E3/E4 decision boundary

These entries update the engineering evidence record only. The scientific acceptance criteria S1–S6 remain open according to their recorded status until the required evidence and review dispositions are supplied.

The following states remain unchanged:

* `freeze_state = NOT_FROZEN`
* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`
* Formal calibration: `NOT AUTHORIZED`

### E5 — Latest full-path engineering workflow, 2026-10-22

**Status:** PASS FOR THE RECORDED ENGINEERING CONFIGURATION ONLY

* Branch: `review/type1-v4-remediation`
* Tested commit: `2ea541207c7c8be0046327399eac2f146d576ab7`
* Workflow run: `39683638768`
* Job: `119512096300`
* Artifact ID: `12384249797`
* Artifact name: `type1-full-path-equivalence-evidence`
* Artifact ZIP SHA-256 reported by GitHub: `156e6ffa90b7b655f85f208c85e885db45a7f213789e25df30fb7e7fdf9cfd18`
* Workflow result: `success`
* Checkout identity: the job log records the tested HEAD as `2ea541207c7c8be0046327399eac2f146d576ab7`.

The job completed the recorded real runner, merger, and checkpoint-resume test. This is engineering evidence for the tested configuration only.

The artifact ZIP digest is not an individual payload-file digest. The artifact payload has not been independently inspected as part of this ledger entry.

**Limitations:** This entry does not establish formal Type-I calibration, validate every V4 candidate parameter, resolve the V3/V4 matrix-to-runner discrepancy, close the independent statistical review gate, freeze the protocol, authorize confirmatory execution, or support the broader research claim.

The following states remain unchanged:

* `freeze_state = NOT_FROZEN`
* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`
* Formal calibration: `NOT AUTHORIZED`

### E6 — Manifest rejection and full-path workflow evidence — 2026-10-25

**Status:** PASS FOR THE EXACT RECORDED ENGINEERING TESTS ONLY

- Branch: `review/type1-v4-remediation`
- Commit: `f9406420d1ff2416ec76b4ad90a893e629f33555`
- Workflow run: `40150487193`
- Job: `121040837616`
- Workflow result: `success`
- Artifact ID: `12582489398`
- Artifact name: `type1-full-path-equivalence-evidence`
- Artifact ZIP SHA-256:
  `962af7439aa08223c41d924aa4177b374b8ca82bcba1871f3e8dba96a45da9ac`

### Rejection tests

The workflow reports:

- `tests.test_type1_pilot_merge_rejections`: 6 tests passed.
- `tests.test_type1_pilot_manifest_rejections`: 2 tests passed.

The manifest tests reject a manifest/run-identity mismatch and a
shard artifact whose bytes no longer match its recorded SHA-256.

### Full-path pilot test

- Test: `tests.test_type1_full_path_equivalence`
- Result: 1 test passed
- Recorded duration: 296.152 seconds
- Outer replicate indices: 0 through 5
- Surrogates per attempt: 200

The integration test exercises the real exploratory pilot runner,
shard execution, merge, reverse-order merge, and checkpoint resume.

### Scope and limitations

This is engineering evidence for the exact recorded test configuration.
The six outer replicates and 200-surrogate setting do not establish
production equivalence at 1,000 surrogates or formal Type-I calibration.

The production runner has not yet been shown to provide the complete
shard, verified-resume, manifest, and merge contract required by this
acceptance plan.

The artifact ZIP digest identifies the uploaded archive; it is not a
claim that every payload file has been independently inspected.

The following states remain unchanged:

- `freeze_state = NOT_FROZEN`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- Formal calibration: `NOT AUTHORIZED`

E6 closes only the two pilot manifest rejection-test items and records
the latest pilot full-path run. It does not close the production-path
or scientific acceptance gates.

### E7 — Official-runner engineering equivalence at B=1000 — 2026-10-26

Status: PASS FOR THE EXACT RECORDED ENGINEERING CONFIGURATION ONLY

- Repository: "AhmedPeaRL/maximal-one"
- Branch: "review/type1-v4-remediation"
- Tested commit: "38694ecdc4bc44a48b86ab8a54221a5d67d6a89c"
- Workflow: "Type-I V4 Official Runner Engineering Equivalence"
- Workflow file: ".github/workflows/type1-v4-engineering-equivalence.yml"
- Workflow run: "40352081420"
- Job: "121674545367"
- Workflow result: "success"
- Checkout identity verification: passed
- Python: "3.11.15"
- Dependency installation: "requirements-lock.txt" with "pip --require-hashes"
- Artifact ID: "12663848472"
- Artifact name: "type1-v4-official-runner-engineering-40352081420-1"
- Artifact size reported by GitHub: 20,217 bytes
- Full-path test duration: 868.804 seconds

Tests reported by the inspected job log

- "tests/test_type1_execution_artifacts.py": 8 tests passed.
- "tests/test_type1_execution_merge_rejections.py": 6 tests passed.
- "tests/test_type1_full_path_equivalence.py": 1 test passed.

Exact test configuration

- Scenario: "gaussian_ar2_phi_0_45_minus_0_10_n3328"
- Replicate indices: 0 through 5; six total.
- Sample size: 3328.
- Master seed: 20261021.
- Requested surrogates per replicate: 1000.
- Execution paths: connected run; two disjoint shards; normal-order merge; reverse-order merge; interruption after two attempts; verified resume.

The integration test compared canonical per-replicate records across connected, merged, reverse-merged, and resumed execution. It required "formal_calibration_pass" to remain false.

Scope and limitations

This establishes engineering path-equivalence evidence for the exact bounded test above. It used the runner's "--engineering-test" mode; it is not a formal confirmatory run through the formal authorization path.

The uploaded artifact ZIP payload has not been independently inspected for this entry. No ZIP SHA-256 is asserted.

This result does not establish Type-I error calibration, approve an acceptance threshold, validate all nine candidate scenarios, approve or freeze the V4 scientific design, establish independent empirical replication, or support the broader HCM claim.

The following states remain unchanged:

- "freeze_state = NOT_FROZEN"
- "confirmatory_execution_authorized = false"
- "claim_support = false"
- "promotion_authority = false"
- Formal calibration: "NOT AUTHORIZED"

E7 closes only the engineering-test items explicitly covered by the recorded tests. Independent statistical review and scientific acceptance gates remain open.

### E8 — Resume identity rejection tests and engineering workflow verification — 2026-10-26

Status: PASS FOR THE RECORDED ENGINEERING TESTS ONLY

- Branch: "review/type1-v4-remediation"
- Tested commit: "a4b8698517c742a8bc5d579418d05c833462c87e"
- Official-runner workflow run: "40378112715"
- Job: "121766644902"
- Result: "success"
- Engineering artifact ID: "12678142523"
- Full-path workflow run: "40378112711"
- Full-path job: "121766644597"
- Full-path result: "success"
- Full-path artifact ID: "12678977860"

The workflow successfully ran the standalone resume identity/artifact rejection tests and the official-runner engineering-equivalence test. The standalone tests use synthetic fixtures and validate the identity-verification helper; they do not by themselves prove that every production CLI resume mismatch is rejected or that every rejected resume preserves an existing checkpoint unchanged.

E8 supplements E7; it does not replace the historical record of earlier failures. Only the exact tests and configurations observed in these runs are considered passed.

This entry does not establish Type-I calibration, approve an acceptance threshold, freeze the V4 protocol, authorize confirmatory execution, establish independent replication, or support the broader HCM claim.

Keep "freeze_state = NOT_FROZEN", "confirmatory_execution_authorized = false", "claim_support = false", and "promotion_authority = false". Formal calibration remains "NOT AUTHORIZED".

## E9 — Resume identity and independent-runner evidence — 2026-10-27

Status: PARTIAL ENGINEERING PASS; PARALLEL WORKER-ORDER RETEST OPEN

- CLI resume identity rejection: PASS for 19 tested identity fields.
- Checkpoint and manifest byte preservation: PASS for tested rejections.
- Independent-runner comparison: PASS for the six declared replicates.
- Comparison artifact: `12719509424`.
- Concurrent worker-order test: FAILED in run `40474378251`;
  a corrected retest is required.
- Cross-runner result does not replace the failed worker-order test.

The V4 matrix remains a candidate, not a frozen protocol.
No acceptance threshold is approved by this entry.

Keep:
- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

Historical failures and classifications must be preserved.

### E14 — Official CLI resume identity and worker-order verification — 2026-10-27

**Status:** PASS FOR THE RECORDED ENGINEERING CONFIGURATIONS ONLY

#### A. Official CLI resume identity rejection

- Repository: `AhmedPeaRL/maximal-one`
- Branch: `review/type1-v4-remediation`
- Tested commit: `eae6f282031c691c9801c1815f41bbf55a244956`
- Workflow run: `40585881657`
- Job: `122478074710`
- Workflow result: `success`
- Workflow attempt: `2`
- Test: `tests/test_type1_cli_resume_identity_rejections.py`

The test creates a valid engineering checkpoint and manifest, records their original bytes and SHA-256 hashes, and tests rejection of each of 19 identity-field mismatches through the actual CLI resume entry point.

For every tested mismatch, the test requires:
- Exit code `1`.
- The expected identity-mismatch diagnostic.
- Byte-for-byte preservation of the original checkpoint.
- Byte-for-byte preservation of the original manifest.
- Matching before/after SHA-256 values for both files.

The workflow reports successful completion of the CLI identity-rejection test. The uploaded artifact payload has not been independently inspected for this ledger entry.

#### B. Concurrent worker-order equivalence

- Workflow run: `40585881668`
- Workflow: `Type-I V4 Cross-Runner Worker-Order Equivalence`
- Tested commit: `eae6f282031c691c9801c1815f41bbf55a244956`
- Result: `success`
- Connected reference: six replicate indices, `0–5`.
- Independent workers: one assigned replicate per worker, with separate artifacts and manifests.
- Scenario: `gaussian_ar2_phi_0_45_minus_0_10_n3328`
- Sample size: `3328`
- Master seed: `20261021`
- Requested surrogates per replicate: `1000`

The workflow reports successful completion of the connected reference, all six worker jobs, and the final worker-to-reference comparison.

The worker-order test compares, by replicate index:
- DGP and null seed identities.
- Generated-series SHA-256.
- Endpoint estimate.
- Requested and valid surrogate counts.
- Exceedance count and Monte Carlo p-value.
- Selected order and diagnostic fields.
- Attempt status and failure reason.

It checks that every requested index is represented exactly once and that the compared scientific fields match the connected reference.

#### C. Scope and governance

These results establish engineering evidence for the recorded test configurations only. They do not establish formal Type-I calibration, approve the V4 acceptance rule, validate all nine scenarios, or support the broader HCM scientific claim.

The tests use `--engineering-test`. They are not an authorized confirmatory execution.

Keep all of the following unchanged:

- `freeze_state = NOT_FROZEN`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- Formal calibration: `NOT AUTHORIZED`

Historical failures remain preserved under their original decision rules. The uploaded artifact payloads and their internal evidence files must be inspected before making stronger claims about artifact contents.

## E15 — CLI identity rejection and independent-runner comparison — 2026-10-27

Status: PASS FOR RECORDED ENGINEERING CONFIGURATIONS ONLY

### A. Official CLI resume identity rejection

- Repository: `AhmedPeaRL/maximal-one`
- Branch: `review/type1-v4-remediation`
- Tested commit: `eae6f282031c691c9801c1815f41bbf55a244956`
- Workflow run: `40585881657`
- Job: `122478074710`
- Workflow result: `success`
- Test: `tests/test_type1_cli_resume_identity_rejections.py`
- Artifact: `12773333354`
- Artifact digest reported by GitHub:
  `sha256:3547b3440c215eeef61b60a6837077bcb8e7db222136590d1a2c50ce002fb34a`

The job log reports successful execution of the official CLI resume identity test.

The test creates an engineering checkpoint and manifest, records their original bytes and SHA-256 hashes, and tests 19 identity-field mismatches individually through the CLI resume path.

For each tested field, the test requires:
- Exit code `1`.
- The expected identity-mismatch diagnostic.
- Byte-for-byte preservation of the checkpoint.
- Byte-for-byte preservation of the manifest.
- Matching before/after SHA-256 values.

The mismatch is injected through the explicit test-only CLI option
`--test-identity-mismatch-field`. Therefore, this evidence establishes rejection through the tested CLI path and test hook, not exhaustive coverage of every externally altered runtime configuration.

### B. Concurrent worker-order comparison

- Workflow run: `40585881668`
- Tested commit: `eae6f282031c691c9801c1815f41bbf55a244956`
- Test: `tests/test_type1_parallel_worker_order_equivalence.py`
- Result: `success`
- Scenario: `gaussian_ar2_phi_0_45_minus_0_10_n3328`
- Sample size: `3328`
- Master seed: `20261021`
- Requested replicates: indices `0–5`
- Requested surrogates per replicate: `1000`
- Declared worker submission order: `[4, 1, 5, 0, 3, 2]`
- Maximum concurrent workers: `3`

The test compares the connected reference against concurrent CLI workers using the declared scientific fields, including seed identities, generated-series SHA-256, endpoint estimate, surrogate counts, exceedances, Monte Carlo p-value, selected order, diagnostics, status, and failure reason.

The test requires exact index coverage and rejects duplicate worker results or invalid attempts.

Qualification: the tested permutation changes submission order while retaining each replicate's own index-specific execution. It does not by itself establish invariance under every possible replicate-to-worker assignment.

### C. Separate GitHub-hosted runner comparison

- Workflow run: `40585881668`
- Comparison job: `122480861674`
- Result: `success`
- Connected reference and six worker jobs: reported successful
- Comparison artifact: `12771342690`
- Comparison artifact digest reported by GitHub:
  `sha256:e1c77bdb04bebf3b8406eb4fcb2aa55d5c2a646bcf779516723be880b1477f34`

The workflow reports successful comparison of the six declared replicate records against the connected reference.

The artifacts have not been independently unpacked and inspected for this ledger entry. The recorded artifact digests establish the GitHub-reported artifact identities, not independent validation of every payload field.

### D. Remaining engineering gates

Keep open:
- Explicit replicate-to-worker assignment permutation across separate jobs.
- Alternative shard partitions beyond those already exercised.
- Exhaustive verification of every execution-identity mismatch path.
- Full branch-by-branch inventory of V3/V4 and `0.075` references.
- Attributable independent human statistical review.
- Prospective acceptance-rule decision and protocol freeze.

### E. Scientific and governance boundary

These results are engineering evidence only. They do not establish Type-I calibration, validate all nine V4 scenarios, approve an acceptance threshold, or support the broader HCM claim.

Keep:
- `freeze_state = NOT_FROZEN`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- Formal calibration = `NOT AUTHORIZED`

Historical failures and their original classifications remain unchanged.

### E15 — Official CLI resume identity rejection — 2026-10-29

**Status:** PASS FOR THE RECORDED ENGINEERING TEST ONLY

- Repository: `AhmedPeaRL/maximal-one`
- Branch: `review/type1-v4-remediation`
- Tested commit: `f88c7918c36f09953dd129cf45bddcadb75fde0c`
- Workflow: `Type-I V4 Official CLI Resume Identity Audit`
- Workflow file: `.github/workflows/type1-v4-cli-resume-identity.yml`
- Workflow run: `40778431846`
- Job: `123133645396`
- Result: `success`
- Test module: `tests.test_type1_resume_cli_identity_rejections`
- Test result: 1 unittest passed
- Recorded test duration: 102.735 seconds
- Artifact ID: `12855647378`
- Artifact name: `type1-v4-cli-resume-identity-40778431846-1`
- Artifact size reported by GitHub: 15,963 bytes
- Artifact ZIP SHA-256 reported in the job log:
  `faeb166fb43b25a59fb04ea0da978a7254852c7a766f5a0c9b4c2f8c34e9be0b`

#### Exact test scope

The test creates a bounded engineering checkpoint and manifest, then
attempts resume after changing each of 19 declared identity fields:

- protocol and scenario identity;
- scenario coefficients;
- sample size, burn-in, and requested surrogate count;
- total repetitions and requested index range;
- master seed and seed schedule;
- commit, matrix, runner, and dependency-lock identities;
- endpoint and null implementation identities;
- Python version and platform identity.

The inspected test implementation requires each changed identity to
produce a nonzero exit code and checks that the checkpoint and manifest
remain byte-for-byte unchanged. It records command output and exit code
in per-case logs.

#### Qualification

This specific workflow test does not itself require exit code `1` or
the exact expected rejection diagnostic. Those stronger assertions are
required in the follow-up test remediation before the gate is considered
fully closed.

The artifact ZIP digest above identifies the uploaded archive; the
archive payload has not been independently inspected for this entry.

#### Decision boundary

This is engineering evidence for the recorded configuration only.
It is not Type-I calibration, acceptance-rule approval, protocol freeze,
or authorization for confirmatory execution.

Keep:

- `freeze_state = NOT_FROZEN`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- Formal calibration: `NOT AUTHORIZED`

## 3. Scientific acceptance criteria

### S1 — Attributable independent statistical review

Status: BLOCKED

Required evidence:
- Named human reviewer with relevant statistical expertise.
- Review date and reviewed commit SHA.
- Written assessment of the estimand, null model, endpoint, design,
  error-rate criterion, Monte Carlo precision, and failure conditions.
- Explicit responses to the unresolved questions in the V4 review brief.

AI-generated analysis must not be represented as independent human approval.

### S2 — Reconcile sample-size and burn-in specifications

Status: BLOCKED PENDING REVIEW

The V4 scenario matrix uses its declared sample-size and burn-in
settings. Any conflicting earlier candidate specification must be
identified and resolved prospectively before protocol freeze.

Required evidence:
- Exact competing specifications and source commits.
- Scientific rationale for the selected values.
- Sensitivity analysis where appropriate.
- Reviewer disposition and approved protocol revision.

### S3 — Reconcile pilot and production surrogate counts

Status: BLOCKED PENDING REVIEW

The runtime pilot uses 200 surrogates per attempt.
The V4 production-equivalence requirements declare 1,000 requested
surrogates per test.

The pilot count must not be silently substituted for the production count.
The production path and the intended Monte Carlo decision rule must be
explicitly validated before formal execution.

### S4 — Justify the Type-I acceptance criterion

Status: BLOCKED PENDING REVIEW

The proposed criterion involving a one-sided 95% Wilson upper bound
and threshold 0.075 must receive a prospective statistical rationale.

Required evidence:
- The target error-rate estimand.
- The rationale for the acceptance boundary and confidence level.
- The planned number of outer repetitions and resulting precision.
- The treatment of invalid attempts and multiplicity across scenarios.
- A documented independent reviewer disposition.

Do not alter thresholds after observing outcomes merely to obtain a pass.

### S5 — Confirmatory null and scenario matrix

Status: BLOCKED

The matrix remains a draft.
The confirmatory null, endpoint, scenario roles, exclusions, and decision
rules must be reviewed and frozen as a single versioned specification.

### S6 — Independent replication and provenance

Status: BLOCKED UNTIL EVIDENCE IS PRODUCED

Each proposed replication domain requires auditable source provenance,
time integrity, eligibility criteria, transformations, null adequacy,
and an explicit inclusion or exclusion decision.

Do not convert UNKNOWN or pending evidence into a negative result
or an eligibility pass.

## 4. Freeze gate

V4 must remain NOT_FROZEN until all required scientific criteria have
documented dispositions, an attributable independent human review
has been completed, and the reviewed protocol snapshot is identified
by commit SHA and content hashes.

## 5. Formal execution gate

Formal calibration requires a separate, explicit, versioned authorization
after the freeze decision.

The engineering pilot does not grant that authorization.

Until the separate authorization is recorded:

- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

## 6. Change control

Every acceptance decision must identify:
- Criterion ID
- Status
- Evidence URI or artifact ID
- Exact commit SHA
- Reviewer identity and date, where applicable
- Rationale and unresolved limitations

Never backdate approval or infer approval from a successful CI run.
