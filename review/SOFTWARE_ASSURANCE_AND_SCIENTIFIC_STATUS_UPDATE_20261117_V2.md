# Software Assurance and Scientific Status Update — 2026-11-17 V2

- Repository: AhmedPeaRL/maximal-one
- Review branch: review/type1-v4-remediation
- Current review HEAD: bbfb99876824bb96a4753bf3ac19a932465aee6d
- Latest manual remediation commit: 94bbbf256fcd07be8511daac7eddfb74abc48a62
- Main HEAD: 9749de9253f144eeda9e1b60cb219cfc5f201ecc
- Pinned human-review target: ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876

Status: REVIEW_ONLY — SOFTWARE_REMEDIATION_OPEN — SCIENTIFIC_GATES_OPEN — NO_NEW_SNAPSHOT

## 1. Branch identity and governance

The review branch is currently at bbfb99876824bb96a4753bf3ac19a932465aee6d.

Commit bbfb998 is an automated requirements-lock refresh whose parent is
94bbbf256fcd07be8511daac7eddfb74abc48a62. Its only changed file is
requirements-lock.txt.

The main branch remains at 9749de9253f144eeda9e1b60cb219cfc5f201ecc.

The branches are divergent. No merge, rebase, force-push, or main-branch
modification is authorized by this update.

The pinned scientific and human-review target remains:
ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876.

No newer human-review snapshot is issued.

## 2. Dependency refresh and OSV inventory

- Workflow run: 44124783809
- Workflow: .github/workflows/replication.yml
- Dispatched branch: review/type1-v4-remediation
- Workflow-definition commit: 94bbbf256fcd07be8511daac7eddfb74abc48a62
- Exact scan target: bbfb99876824bb96a4753bf3ac19a932465aee6d

The following stages succeeded:
- Review-branch guard.
- Python 3.11.15 dependency refresh.
- Hash-lock generation.
- Clean-environment installation using --only-binary and --require-hashes.
- pip check.
- Import smoke test.
- compileall.
- Unit tests.
- Publication of requirements-lock.txt to the review branch.
- OSV inventory execution.

The refresh manifest reports:
- pip-tools 7.6.2.
- pip_check: PASS.
- import_smoke_test: PASS.
- compileall: PASS.
- unit_tests: PASS.

The OSV inventory scanned six supported manifests/lockfiles.
Each requirements manifest resolved 47 packages.
The OSV JSON result contained zero vulnerability findings.

This result applies to the exact scanned lock and does not establish that
future dependency changes are vulnerability-free.

## 3. Exact-commit software assurance

The exact-commit assurance job did not pass.

Actionlint:
- Two reusable-workflow reference diagnostics.
- Both involve the local "$/.github/workflows/..." syntax.
- The pinned actionlint 1.7.12 rejects these references.
- The selected remediation is "./.github/workflows/..." for compatibility
  with the pinned scanner.

Zizmor:
- Two artipacked findings.
- Locations:
  .github/workflows/evaluation.yml
  .github/workflows/scientific-evaluation.yml
- Both checkout steps need persist-credentials: false.

Scorecard:
- Overall score: 8.6.
- Vulnerabilities: 10, with zero existing vulnerabilities reported.
- Token-Permissions: 9.
- Security-Policy: 4.
- Fuzzing: 0.
- Pinned-Dependencies: 9.

The software-assurance result remains open until a fresh exact-commit scan
records zero scanner exit codes and the findings are manually reviewed.

## 4. Runtime dependency and module-execution defects

Workflow run 44120444316 failed in verify-core with:

ModuleNotFoundError: No module named 'psutil'

The workflow executes analysis/system_health_check.py, which imports psutil.
The current requirements.in did not declare psutil, and the refreshed lock
therefore omitted it.

The proposed remediation is to declare psutil==7.2.2 in requirements.in
and regenerate the lock through the review-branch dependency-refresh workflow.

Workflow run 44121644472 also exposed a subprocess import-path failure:

ModuleNotFoundError: No module named 'analysis'

The failure occurs when scripts/generate_report.py executes
scripts/canonical_consensus.py by direct file path.

The proposed remediation is to invoke:
python -m scripts.canonical_consensus
with the repository root as the subprocess working directory.

These are runtime engineering defects. Their remediation must not be
represented as scientific evidence or claim support.

## 5. Primary scientific null and model capacity

Workflow run 44120444316 produced a canonical report with:

- Observed primary alpha: 2.525347.
- Primary null: stationary Gaussian AR(p), AIC order selection 1..20.
- Primary null samples: 1,000.
- Primary null mean: 3.197386.
- Primary null p-value: 0.999001.
- Primary null rejection at 0.05: false.
- Selected observed order: 20, the declared maximum.
- Surrogate boundary fraction: 0.947.

The primary stochastic null was not rejected.

The permutation result p=0.0002 is diagnostic-only and is not the
primary inferential result.

The primary null capacity audit in run 44122928330 reported:
- 1,000 valid surrogate refits.
- 937 boundary selections at order 20.
- Boundary fraction: 0.937.
- Model-capacity review triggered.

This does not prove that AR(20) is invalid, nor does it establish AR(40)
as a justified replacement.

No production null-family change or order-cap increase is authorized.

## 6. Null-calibration diagnostic

Workflow run 44122215332 used:
- 50 outer replicates per scenario.
- 200 inner surrogates per outer replicate.
- Seed 90210.
- Diagnostic-only scientific role.

Observed p<0.05 counts:
- AR(1), phi=0.7: 6/50.
- AR(2), phi=0.5, 0.2: 3/50.

These small diagnostic samples are not a formal Type-I calibration
and do not authorize confirmatory use.

The results should be retained for independent statistical review.

## 7. Replication eligibility and domain evidence

The final claim gate in run 44120444316 reported:
- Eligible independent secondary domains: 0.
- Minimum required: 2.
- Claim support granted: false.
- Promotion authority granted: false.
- Scientific claim status: under_investigation.

HadCET and INDPRO passed their recorded time-integrity checks.
However, provenance approval and replication eligibility remain false.

Measurement validity and time-integrity validity do not establish
independent scientific replication.

Approved independent secondary domains remain 0/2.

## 8. Computational reproducibility boundary

The clean-checkout replay matched the canonical report fingerprint.

The replay used a fresh public repository checkout but the same workflow
runner and execution environment.

The evidence does not establish:
- Independent laboratory replication.
- Independent implementation replication.
- Independent execution-environment replication.
- Independent scientific replication.

The verified scope is computational reproducibility only.

## 9. Public report retrieval

The public report retrieval audit in run 44120444316 returned HTTP 404
for the expected public report hash and canonical report paths.

Public retrieval remains unverified.

This is a publication/retrieval issue, not a scientific result.

## 10. Independent human reviews

Four attributable independent reviews remain pending:

1. Statistical methods and null-model adequacy.
2. Climate-domain independence and HadUKP/HadCET suitability.
3. Econometric-domain independence and CPIAUCNS/INDPRO suitability.
4. GitHub Actions and CI/CD security.

No automated or AI-generated report substitutes for an attributable
independent human decision.

## 11. Non-authorization

The following remain unchanged:

- protocol_freeze = NOT_FROZEN
- formal_calibration_authorized = false
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- approved_independent_secondary_domains = 0
- replication_status = 0/2

This update records software and scientific evidence only.

It does not authorize a new human-review snapshot, protocol freeze,
formal Type-I calibration, confirmatory execution, claim promotion,
or any modification to main.
