# Exact-Commit Software Assurance Review Addendum
## 2026-11-20 — Run 44714620618

### 1. Repository and exact identity

Repository: AhmedPeaRL/maximal-one

Target branch:
review/type1-v4-remediation

Exact scan commit:
d1ac0f52dd3c711595d1364ca7a2a5bd671eb49c

Workflow:
.github/workflows/replication.yml

Workflow run:
44714620618

The scan manifest confirms:
- scan_commit = d1ac0f52dd3c711595d1364ca7a2a5bd671eb49c
- workflow_definition_commit = d1ac0f52dd3c711595d1364ca7a2a5bd671eb49c
- workflow_ref = refs/heads/review/type1-v4-remediation

### 2. Execution result

| Job | Result |
|---|---|
| guard | success |
| review-head | success |
| refresh | skipped |
| publish | skipped |
| exact-assurance | failure |
| nested OSV inventory | success |

The assurance-only path did not execute dependency refresh or publishing.

The reusable workflow call chain was exercised by GitHub Actions:
- replication.yml invoked software-assurance-exact-commit-v1.yml
- software-assurance-exact-commit-v1.yml invoked dependency-vulnerability-inventory.yml
- the nested OSV inventory job completed successfully

### 3. Scanner results

#### actionlint 1.7.12

Result: NOT PASSED

The report contains exactly two diagnostics concerning the documented
GitHub same-repository reusable workflow syntax:

- replication.yml:428
- software-assurance-exact-commit-v1.yml:24

Both use the `$/` syntax.

The actionlint output identifies the syntax as unsupported by actionlint
1.7.12. The GitHub Actions runtime successfully resolved the calls in
this run.

The recorded actionlint exit code is 123 from xargs.

Required remediation:
- retain the GitHub-supported `$/` references
- add narrowly scoped path-specific actionlint configuration
- pass the exact target configuration file to actionlint
- keep all unrelated actionlint checks enabled

#### zizmor 1.30.1

Result: PASS

- exit code: 0
- zizmor.json: []
- no findings were returned

No broad audit suppression is authorized.

#### OpenSSF Scorecard 5.6.0

Result: COMPLETED

Overall score: 8.7

| Check | Score |
|---|---:|
| Binary-Artifacts | 10 |
| Dangerous-Workflow | 10 |
| Dependency-Update-Tool | 10 |
| Fuzzing | 0 |
| License | 9 |
| Packaging | 10 |
| Pinned-Dependencies | 9 |
| SAST | 10 |
| Security-Policy | 4 |
| Token-Permissions | 10 |
| Vulnerabilities | 10 |

Pinned-Dependencies details:
- GitHub Actions: 211/211 pinned
- Container images: 0/1 pinned
- npm commands: 4/7 pinned
- pip commands: 30/47 pinned

The complete reported locations are preserved in:
evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261120.csv

Security-Policy remains open because no valid reporting URL or email
was found in SECURITY.md.

Fuzzing remains an optional engineering gap, not a detected vulnerability.

License remains open because the MIT license text is followed by
additional project-specific text.

#### OSV-Scanner 2.7.1

Result: PASS WITH LIMITED SCOPE

- exit code: 0
- osv.json results: []
- six supported manifests/lockfiles scanned
- five Python manifests reported 48 packages each
- package-lock.json reported zero packages

This result does not establish the absence of vulnerabilities in
Docker base-image or operating-system packages.

### 4. Authority and scientific status

The assurance manifest records:

- protocol_freeze = NOT_FROZEN
- formal_calibration_authorized = false
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- authority = NONE

This run is software assurance evidence only.

It is not:
- formal Type-I calibration
- confirmatory scientific execution
- independent replication
- scientific claim validation
- promotion authorization

### 5. Branch isolation

The main branch comparison reports:

main:
9749de9253f144eeda9e1b60cb219cfc5f201ecc

review branch:
review/type1-v4-remediation

Comparison:
- 651 commits ahead
- 36 commits behind
- branches diverged

No merge or cherry-pick is authorized.

The main branch remains outside the remediation scope.

### 6. Required next actions

1. Add .github/actionlint.yaml with only the two exact compatibility
   exceptions.
2. Pass the target actionlint configuration explicitly in the
   exact-commit assurance workflow.
3. Remediate verified Pinned-Dependencies locations without changing
   the scientific protocol.
4. Improve SECURITY.md without inventing a response-time SLA or
   unverified contact address.
5. Separate the canonical MIT license from the HCM project statement.
6. Correct the invalid Dependabot ecosystem configuration if monthly
   update PRs are approved.
7. Assess Docker base-image and OS-package vulnerabilities separately.
8. Update the residual register from the next exact-commit artifact.

### 7. Next execution authorization

No workflow is authorized until the exact remediation commit is
reviewed.

After review, the only permitted workflow is:

.github/workflows/replication.yml

Target branch:
review/type1-v4-remediation

Required input:
assurance_only = true

Expected:
- guard: success
- review-head: success
- refresh: skipped
- publish: skipped
- exact-assurance: success
- OSV inventory: success

If assurance_only is missing or unchecked, cancel the run.

No scientific workflow, calibration workflow, snapshot workflow,
promotion workflow, dependency-refresh mode, or main-branch workflow
is authorized by this addendum.
