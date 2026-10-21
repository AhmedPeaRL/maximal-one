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
