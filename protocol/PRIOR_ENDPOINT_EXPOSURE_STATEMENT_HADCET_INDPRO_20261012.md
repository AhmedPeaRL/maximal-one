# Prior Endpoint Exposure Statement — HadCET and INDPRO

**Record date (UTC):** 2026-10-12  
**Record type:** Researcher statement recorded in project conversation; not a Git commit or external preregistration.  
**Status:** Exposure statement recorded; technical pre-analysis decisions remain incomplete.

## 1. Researcher statement

The researcher states that the endpoint results for HadCET and INDPRO had not been viewed before completion of the secondary-domain pre-analysis protocol.

This statement concerns viewing/inspection. It does **not**, by itself, establish whether endpoint computations had already run automatically, whether values were present in workflow logs or artifacts, or whether any other collaborator or process inspected them. Those questions must not be silently inferred from the statement.

## 2. Classification rule

- **Viewed before protocol completion:** No, according to the researcher statement above.
- **Computed before protocol completion:** Not established by this statement; verify against workflow run timestamps, commit SHAs, artifacts, and any available review history before making a stronger claim.
- **Pre-registration status:** Not yet established. A protocol becomes prospectively fixed for this project only after the actual technical decisions are completed and committed before endpoint computation/inspection. Do not backdate a commit or describe post-result amendments as preregistered.
- **HadCET / INDPRO replication approval:** NOT APPROVED pending the completed protocol, provenance review, independence assessment, and null-model adequacy/calibration.
- **Claim-promotion authority:** FALSE.

## 3. Audit trail to complete

Before running or inspecting either endpoint, record the following in a new dated commit:

1. The exact commit SHA and file hash for the completed protocol.
2. Relevant prior GitHub Actions run IDs, commit SHAs, timestamps, and artifact names that could contain endpoint outputs.
3. Whether each output was merely generated, made visible in logs/artifacts, or actually inspected by the researcher. Do not equate these states.
4. The exact endpoint implementation/version, estimator settings, frequency band, normalization, and minimum segment/length requirements copied from the current canonical code.
5. One primary HadCET window rule justified by source/measurement provenance, not observed alpha; list any sensitivity windows now and report them transparently.
6. Exactly one primary INDPRO transformation and its scientific rationale, selected without consulting endpoint outcomes; identify alternatives as sensitivity-only.
7. The null family, fitting/order-selection procedure, and calibration prerequisite. The AR(p) null remains exploratory/not frozen until its adequacy review passes.
8. Provenance and independence review, including whether either candidate can reasonably count as independent replication of the sunspot primary domain.

## 4. Decision safeguards

- Do not compute or inspect HadCET/INDPRO endpoint alpha, p-values, or endpoint plots until the protocol decisions are complete and committed.
- If a historical workflow artifact is found to contain endpoint values, document its generation time and whether/when it was inspected. If the protocol was formed after those values were computed or inspected, classify the analysis conservatively as exploratory/post-observation as appropriate; do not retroactively call it preregistered.
- Keep failed or ineligible candidates in the record with reasons. Do not substitute a new domain after outcome inspection without documenting the selection process.
- The primary stochastic short-memory null remains not rejected in the current record; the current scientific claim remains UNDER_INVESTIGATION with no claim support and no promotion authority.

## 5. Current status

| Item | Status |
|---|---|
| Researcher reports no prior viewing of HadCET/INDPRO endpoint results | RECORDED |
| Whether endpoint computation occurred before protocol completion | NOT ESTABLISHED — AUDIT REQUIRED |
| Completed technical pre-analysis decisions | PENDING |
| HadCET replication eligibility | NOT APPROVED |
| INDPRO replication eligibility | NOT APPROVED |
| Claim support / promotion authority | FALSE |
