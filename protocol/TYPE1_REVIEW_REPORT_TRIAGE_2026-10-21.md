# Type-I V4 — Review Report Triage

**Date:** 2026-10-21
**Repository:** `AhmedPeaRL/maximal-one`
**Working branch:** `review/type1-v4-remediation`
**Reference commit available at triage:** `f16759a59aae272a037adbb1bb865be860acab87`
**Protocol:** `HCM_TYPE1_CALIBRATION_V4_DRAFT`

## 1. Purpose

This record triages two submitted review texts, designated Report A and Report B. It does not replace the required attributable independent statistical review, approve the protocol, freeze V4, authorize confirmatory execution, or support the broader research claim.

The reports are retained as submitted. Their substantive statements are not treated as verified findings unless supported by a specific reviewed artifact, analysis, or reproducible result.

## 2. Attribution status

The submitted text does not itself provide enough information to complete the repository's required attribution record.

Pending documentation, record:

* Reviewer identity: NOT DOCUMENTED IN THE SUBMITTED TEXT
* Relevant statistical expertise: NOT DOCUMENTED IN THE SUBMITTED TEXT
* Review date: NOT DOCUMENTED IN THE SUBMITTED TEXT
* Exact reviewed commit SHA: NOT DOCUMENTED IN THE SUBMITTED TEXT
* SHA-256 hashes of reviewed files: NOT DOCUMENTED IN THE SUBMITTED TEXT
* Conflict-of-interest declaration: NOT DOCUMENTED IN THE SUBMITTED TEXT
* Final signed or otherwise attributable disposition: NOT DOCUMENTED IN THE SUBMITTED TEXT

These fields being undocumented here does not establish that the reviewers lack the relevant qualifications or independence. Obtain the missing information from the submitters; do not infer or fabricate it.

## 3. Report A — substantive triage

**Disposition:** `REVISE_AND_RESUBMIT` for purposes of closing the V4 review gate.

The report correctly identifies the broad relevance of the endpoint, null model, Type-I error, Monte Carlo simulation, uncertainty, burn-in, and reproducibility.

The following matters remain unresolved:

1. The endpoint is described generically rather than assessed against the exact V4 endpoint implementation and its invalid-input rules.
2. The displayed empirical-alpha formula does not adequately distinguish inner surrogate generation from outer null repetitions in which the entire test procedure is executed.
3. The recommendation of at least 1,000 surrogates is not accompanied by a quantitative justification tied to the chosen p-value procedure and required precision.
4. The proposed acceptance principle does not justify the historical 0.075 upper-bound ceiling or settle the number of outer repetitions.
5. The report does not issue explicit dispositions on the V4 null specification, scenario-specific interpretation, invalid attempts, shard integrity, or the required production-path equivalence evidence.
6. The resonance discussion proposes general remedies but does not decide whether the existing prespecified scenarios and endpoint meet the stated scientific objective.

No unresolved item is deemed closed by this report alone.

## 4. Report B — substantive triage

**Disposition:** `REVISE_AND_RESUBMIT` for purposes of closing the V4 review gate.

The report usefully discusses false-positive control, Monte Carlo uncertainty, autocorrelation, scenario stability, and reproducibility.

The following matters remain unresolved:

1. The report does not identify the exact reviewed commit or provide file-level hashes and a reviewable record of attribution.
2. The endpoint and null model are described mainly through examples rather than through explicit decisions on the V4 implementation.
3. The report does not justify the proposed 0.075 acceptance ceiling or specify the complete statistical decision rule.
4. The invalid-attempt policy, required number of valid surrogates, failed-fit handling, and missing-evidence policy are not resolved.
5. The recommendation to proceed to a final confirmatory run conflicts with the current V4 draft state and the still-open acceptance criteria.
6. The report does not document the required end-to-end equivalence evidence for fresh execution, connected execution, sharding, reverse-order merging, and verified resume under the approved production specification.

The recommendation to run confirmatory calibration is therefore not accepted as authorization.

## 5. Required next review submission

Request an attributable, version-specific disposition that explicitly addresses every section of:

`protocol/TYPE1_INDEPENDENT_REVIEW_BRIEF_V1.md`

The submission must include:

* Reviewer identity and relevant expertise.
* Review date and exact reviewed commit SHA.
* SHA-256 hashes of all reviewed protocol and implementation files.
* A section-by-section disposition: `APPROVE`, `APPROVE_WITH_SPECIFIED_CONDITIONS`, `REVISE_AND_RESUBMIT`, `REJECT`, or `NOT_REVIEWED`.
* A written rationale for the endpoint, null model, scenarios, Type-I acceptance rule, Monte Carlo precision, invalid-attempt policy, computational feasibility, and equivalence evidence.
* Explicitly stated conditions and unresolved issues.

Do not represent AI-generated analysis as independent human approval. AI-assisted analysis may be retained as supporting material, clearly labeled as such.

## 6. Current gate decision

* Independent review gate: `NOT_CLOSED`
* Protocol freeze: `NOT_FROZEN`
* Confirmatory execution: `NOT_AUTHORIZED`
* Claim support: `false`
* Promotion authority: `false`

This triage is a documentation decision, not a calibration result.

No confirmatory outcomes may be inspected to tune the acceptance threshold, scenario definitions, exclusions, or invalid-attempt policy.
