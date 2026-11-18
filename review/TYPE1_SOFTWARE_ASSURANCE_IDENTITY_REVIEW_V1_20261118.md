# Type-I Software Assurance Identity Review — 2026-11-18

## Status

- AUTOMATED_TECHNICAL_EVIDENCE_REVIEW.
- NOT_AN_INDEPENDENT_HUMAN_AUDIT.
- NO_FINDING_CLOSURE_AUTHORITY.
- NO_SCIENTIFIC_PROMOTION_AUTHORITY.

## 1. Repository and branch identity

Repository: AhmedPeaRL/maximal-one

Main comparison commit:
9749de9253f144eeda9e1b60cb219cfc5f201ecc

Review commit supplied for this review:
81aa3aecda94edc971b9e750f32de801717dc696

The review branch remains divergent from main.
No merge, rebase, force-push, or main-branch modification is authorized.

## 2. Exact-target software assurance evidence

Workflow:
.github/workflows/type1-software-assurance-v3.yml

Workflow run:
44182949661

Artifact ID:
14372144011

Artifact name:
type1-software-assurance-v3-44182949661-1

Artifact ZIP SHA-256:
f88d5f18b91b0c6b97aa63aef8dc3f9cc4c7f3b1de83abce4f07addea72b182c

Scan target:
ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876

Workflow-definition commit:
87160e6469d323187916d375c11300158777d22b

Review-branch commit recorded by the scan:
87160e6469d323187916d375c11300158777d22b

Main comparison commit:
9749de9253f144eeda9e1b60cb219cfc5f201ecc

This scan is not a scan of review commit 81aa3aecda94edc971b9e750f32de801717dc696.

## 3. Snapshot and source identity

- Inventory run: 43757949244
- Inventory artifact: 14178549418
- Inventory artifact SHA-256:
dcb0dd3283689e171c938bce02409b937c431b96ef5a86f44ca9e47fc2413eb4

- Snapshot run: 43762349962
- Snapshot artifact: 14180143511
- Snapshot archive SHA-256:
caa75810be3463ddf09c6d379bd6685337bbee6be62284bf8fc877768b43364e

Snapshot manifest SHA-256:
2ff2e9b8c9aa2aea520ca1612e76a92703af9d479d6742e6ea211627862d9426

Inner snapshot ZIP SHA-256:
6a399450a2e69d3e069363a957200203c84025754cb5b333dc90786e64494842

- Selected files: 289
- Present files: 289
- Extraction verification: PASS

Independent verification in this review:
- 292 internal snapshot checksum entries checked.
- Zero missing or mismatched entries.
- All 14 raw-output hashes in the assurance manifest matched the downloaded artifact.

This establishes a strong source-identity chain for the selected snapshot scope.
It is not a claim that every repository file was independently attested.

## 4. Scanner results

### actionlint 1.7.12

- Exit code: 123
- Diagnostic headers: 97
- ShellCheck diagnostics: 92

Disposition:
OPEN — occurrence-level triage required.

### zizmor 1.30.1

- Exit code: 14
- Total findings: 205

Severity:
- High: 164
- Medium: 37
- Informational: 4

Rule totals:
- unpinned-uses: 151
- excessive-permissions: 19
- artipacked: 18
- template-injection: 13
- dangerous-triggers: 2
- cache-poisoning: 1
- superfluous-actions: 1

Disposition:
OPEN — no automatic closure.

### OpenSSF Scorecard 5.6.0

- Exit code: 0
- Overall score: 5.7

Reported check results include:
- Pinned-Dependencies: 3
- Fuzzing: 0
- Security-Policy: 0
- Token-Permissions: 0
- Vulnerabilities: 0, with reason "73 existing vulnerabilities detected"

The 73-vulnerability statement requires advisory-level triage.
It does not establish severity or exploitability by itself.

## 5. Scorecard identity limitation

The Scorecard JSON records:

repo.name = file:///home/runner/work/_temp/target-source
repo.commit = unknown

The assurance workflow separately validates and materializes the exact target commit.
Therefore, the manifest and workflow logs provide the source-identity evidence.

Scorecard itself does not independently attest the target commit.
This limitation must remain visible in every report derived from this run.

A Scorecard exit code of zero means the tool completed.
It does not mean every Scorecard check passed.

## 6. Zizmor register provenance limitation

The current file:

review/TYPE1_ZIZMOR_205_FINDINGS_REGISTER_V1.csv

references an earlier scan:
- workflow run: 43611097357
- artifact: 14120366991
- manifest SHA-256:
  422c1a1722108b1a74173224af39dd5d043e0f524a1272833210e5d10b638708

The newer assurance evidence is:
- workflow run: 44182949661
- artifact: 14372144011

Both scans identify target commit ad106 and report 205 findings.
The totals and severity distribution match.

However, row-level identity between the older register and the newer raw Zizmor JSON must be verified before updating provenance or declaring a reconciliation complete.

All 205 current register rows remain OPEN_UNREVIEWED and NOT_CLOSED.

## 7. Scientific execution evidence reviewed

Run 44180473104:
- Final claim gate: BLOCKED.
- Eligible independent secondary domains: 0 of 2.
- Strict claim status: under_investigation.
- Claim support granted: false.
- Promotion authority granted: false.

Canonical primary endpoint:
- alpha: 2.525347.
- Primary stationary Gaussian AR(p) null p-value: 0.999001.
- Primary null rejected: false.
- Permutation diagnostic p-value: 0.0002.
- Permutation result remains diagnostic-only.

AR capacity:
- Selected order: 20, the declared maximum.
- Dedicated audit boundary fraction: 0.937.
- Canonical null-gate boundary fraction: 0.947.
- Source-scoped difference is explicitly reconciled.
- Fresh Type-I/null-capacity calibration remains required.

Computational replay is not independent scientific replication.
External laboratory replication and independent implementation replication remain false.

Run 44185145118:
- WDC-SILSO comparison found four field mismatches in January-April 2026.
- Six newer official rows, May-October 2026, were not appended.
- The analysis file was not modified automatically.

Run 44185679041:
- HadUKP EWP passed structural checks but remains pending independence and null review.
- FRED CPIAUCNS failed missingness checks because one value is missing.
- No endpoint computation was performed.
- Approved independent secondary domains: zero.

## 8. Execution history limitation

The existing POST-V9 Addendum V1 records selected executions.
It does not provide a complete ledger of every later workflow run examined in this review.

A separate append-only run-activity ledger is required.
The original Addendum V1 must not be silently rewritten.

## 9. Human review status

The four requested independent reviews remain pending.
Acknowledgements and out-of-office messages are not approvals.

No new reviewer snapshot is authorized by this document.

## 10. Final disposition

SOFTWARE_ASSURANCE_STATUS:
OPEN — CURRENT-SOURCE SCAN AND OCCURRENCE-LEVEL RECONCILIATION REQUIRED.

SCIENTIFIC_CLAIM_STATUS:
UNDER_INVESTIGATION.

PROTOCOL_FREEZE:
NOT_FROZEN.

FORMAL_CALIBRATION_AUTHORIZED:
false.

CONFIRMATORY_EXECUTION_AUTHORIZED:
false.

CLAIM_SUPPORT:
false.

PROMOTION_AUTHORITY:
NONE.

This document is an evidence review, not a signed independent human audit.
It closes no software finding and grants no scientific authorization.
