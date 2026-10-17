# Independent Review and Next-Gate Decision — 2026-10-17

**Reviewed repository snapshot:** `3ef074c3be702af79d5b449f60deb32b5756439d`
**Scientific status:** `UNDER_INVESTIGATION`
**Claim support:** `false`
**Promotion authority:** `false`
**Confirmatory protocol:** `NOT_FROZEN`
**Approved independent secondary domains:** `0/2`

## 1. Decision

Preserve the current scientific gates and historical failures. Do not compute candidate confirmation endpoints, change the acceptance rule, impute missing candidate observations, or promote the claim.

The latest available workflow evidence supports further diagnostic and source-audit work only. It does not establish scientific replication or claim support.

## 2. Verified workflow outcomes

### 2.1 Main computational workflow

Run: `39057646287`
Commit reported by the final gate: `3ef074c3be702af79d5b449f60deb32b5756439d`

The supporting computational jobs completed successfully, but the final claim and workflow gate returned:

* `status = BLOCKED`
* `eligible_replication_domain_count = 0`
* `minimum_replication_domains = 2`
* `claim_support_granted_by_this_job = false`
* `promotion_authority_granted_by_this_job = false`

Run URL: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39057646287

### 2.2 Prospective raw-source audit

Run: `39057735852`
Artifact: `12109822270`
Artifact ZIP SHA-256: `24bc00b6f8a7ee58d05ed5600bbf26fc09fdea91b7601b23957649ccf086b8a9`

The audit acquired and preserved both source snapshots. It did not calculate candidate endpoints.

**HadUKP EWP monthly precipitation**

* Audit window: `1913-01-01` through `2025-12-01`, inclusive
* Rows: `1356`
* Missing or non-finite values: `0`
* Monthly timestamp/cadence checks: passed
* Raw SHA-256: `eb2a20081a4673211783b0fe442007921d0f23a4683065954373c6ce0fa96637`
* Parsed-data SHA-256: `3c757cd2f7258944ba393906ea3fd7294b48a09782319381f91d9117652b87df`
* Decision: `STRUCTURAL_CHECKS_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW`

This is a structural result only. Independence, shared nuisance, source-vintage review, global prior-endpoint exposure, and null adequacy remain unresolved.

**FRED CPIAUCNS monthly CPI**

* Audit window: `1913-01-01` through `2025-12-01`, inclusive
* Rows: `1356`
* Missing or non-finite values: `1`
* Missing observation date: `2025-10-01`
* Valid numeric observations: `1355`
* Monthly timestamp/cadence checks: passed
* Raw SHA-256: `2f72ee1766c487a1ab631bfcf161ef6743858e59a331b57da36d89c5496f7fa0`
* Parsed-data SHA-256: `96a5ee8dd09088f3be7d710cb9969df2ac6bb493dc9434d87be4ee4412ae5348`
* Decision: `STRUCTURAL_AUDIT_BLOCKED`

Retain the exact raw snapshot. Do not insert an estimated value, interpolate, silently drop the month, or change the eligibility policy after seeing the result. Any later source retrieval must be preserved as a separate dated snapshot with its own SHA-256.

Run URL: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39057735852

### 2.3 Claim-promotion workflow

Run: `39057767292`

The `Claim Promotion Gate` failed. The current independent replication requirement remains unmet. A failed promotion gate must not be weakened to make the workflow green.

Run URL: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39057767292

## 3. Type-I calibration decision

The previously recorded four-scenario calibration contains two passes and two failures under the declared Wilson-interval acceptance rule:

* `gaussian_ar1_phi_0_4`: pass for this scenario
* `gaussian_ar2_phi_0_45_minus_0_10`: fail
* `gaussian_ar5_low_order_coefficients`: pass for this scenario
* `gaussian_ar10_low_order_coefficients`: fail

The previous scenario artifacts were associated with commit `9588084063ed02c456126a51a26fbd1ae992d82d`. A same-commit rerun of all four scenarios on the reviewed commit has not yet been established by the supplied evidence.

Preserve the historical failures and the existing acceptance rule. Do not change thresholds post hoc. Rerunning the declared scenarios on one exact commit is required, but a successful rerun alone will not establish complete null adequacy.

## 4. Mandatory next steps

1. Run the `Null Type-I Calibration (Synthetic Scenarios)` workflow for all four declared scenarios on one exact, identified commit. Preserve every scenario artifact and its hash.
2. Verify the checked-out commit SHA in each job. Do not assume that selecting `main` guarantees the intended commit if the branch head has changed.
3. Independently review null-family adequacy, temporal structure, model-capacity limits, Type-I error, power, fitting failures, and scenario coverage. Do not select a null family based on candidate endpoint values.
4. Keep CPIAUCNS structurally blocked under the current completeness policy unless an independently justified, prospectively documented protocol permits a valid alternative treatment. Do not alter the existing snapshot.
5. Continue the HadUKP source-vintage, prior-endpoint exposure, and shared-nuisance/independence review. Preserve `UNKNOWN` wherever evidence is missing.
6. Complete the global historical endpoint-exposure audit. The existing HadCET/INDPRO audit is explicitly partial; absence of evidence is not proof that an endpoint was never computed or displayed.
7. Freeze the full confirmatory protocol only after independent methods review and calibration acceptance. Record the endpoint, transformation, window, frequency band, test direction/tail, null family, seeds, exclusions, source snapshots, code commit, environment, and review timestamp before calculating candidate endpoints.
8. Only then assess the two required independent real-domain replications under the same frozen protocol. A domain counts only after eligibility, provenance, independence, and domain-level null evidence are all satisfied.

## 5. Non-retroactivity and interpretation

The existing candidate endpoint history must not be relabeled as preregistered confirmation. Structural validity, deterministic computation, internal consistency, and passing engineering jobs do not individually establish scientific replication.

Even a future rejection of a declared stochastic null would constitute evidence against that null under the specified protocol; it would not by itself establish HCM causation, consciousness, universality, mechanism, or a new physical law.

**Final decision:** `HOLD_CONFIRMATORY_ANALYSIS; PRESERVE_FAILURES; RERUN_CALIBRATION_ON_ONE_COMMIT; COMPLETE_INDEPENDENT_NULL_AND_SOURCE_REVIEWS`.
