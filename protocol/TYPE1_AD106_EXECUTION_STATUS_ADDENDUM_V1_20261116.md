# Type-I AD106 Execution Status Addendum V1 — 2026-11-16

**Status:** `V9_BATCH_AND_PREFLIGHT_VERIFIED; TARGET_ASSURANCE_COMPLETED_WITH_OPEN_FINDINGS; CURRENT_BRANCH_SCAN_BLOCKED_BY_VERSION_COMMAND; HUMAN_REVIEW_PENDING; SOURCE_DATA_DISCREPANCY_OPEN`

## 1. Scope and immutable identities

- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Review branch commit at this audit: `ff71f97a1752f2e998ae740d796eae7dfdc0b9f0`
- Main branch commit at this audit: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Exact target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Population register: `protocol/TYPE1_AD106_POPULATION_REGISTER_V9.json`
- Source identity addendum: `protocol/TYPE1_AD106_SOURCE_IDENTITY_ADDENDUM_V8_20261115.json`

This addendum records executions completed after Population Register V9 was prepared. It does not replace historical records or change the scientific protocol.

## 2. Source inventory and snapshot

- Inventory run: `43757949244`
- Inventory artifact: `14178549418`
- Inventory SHA-256: `4ee4335d5807c0a90ac668637a2bd55277ae9b6ce442af316f65f22a24f17a89`
- Target ledger SHA-256: `ad18beccc8e5e9e9934838afe0e176b9e25658bea24e93c5dd3d2ec9ef119c67`
- Main ledger SHA-256: `e2a9aa2b2da293c2c68f0a518ca1d76c5ffc85c8f7304ed17d3e312e1beec650`
- Target occurrence count: 1800
- Main occurrence count: 943

Exact snapshot:

- Snapshot run: `43762349962`
- Snapshot artifact: `14180143511`
- Selected files: 289
- Present files: 289
- Extraction checks: 292
- Missing required paths: 0
- Missing scope paths: 0
- Manual adjudication overlay records: 0

## 3. V9 batch generation

- Workflow: `.github/workflows/type1-target-batch-generation-v4.yml`
- Run: `43769473796`
- Job: `132981944196`
- Artifact: `14184020886`
- Artifact SHA-256: `4dc97cebce9c137368ac4ab0efc1a44d96c4b557ec30fbcd8950ae565751156f`

Verified output:

- 72 batches
- 25 occurrences per batch
- 1800 total occurrences
- 1800 unique occurrence IDs
- All batches bound to inventory SHA `4ee4335d5807c0a90ac668637a2bd55277ae9b6ce442af316f65f22a24f17a89`
- All batches bound to target commit `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

Interpretation: navigation and review preparation only. No adjudication or execution authority.

## 4. V9 human-overlay preflight

- Workflow: `.github/workflows/type1-human-overlay-preflight-v5.yml`
- Internal schema: `HCM_TYPE1_HUMAN_OVERLAY_PREFLIGHT_V6`
- Run: `43769577842`
- Job: `132982272778`
- Artifact: `14183631724`
- Artifact SHA-256: `11c663b608036a0c5bb777367886c89efc45f89e21390910aeb478883b9f34de`

Verified output:

- CSV: `adjudication/incoming/first-three-occurrences-v6.csv`
- CSV SHA-256: `60ddb17002a5e6ccdd82b2680fdb4efcc3ce94724e1c7d48a5fa9e6040fb1c05`
- Rows: 3
- All rows open: true
- All rows pending: true
- Adjudications applied: 0

Interpretation: read-only preflight succeeded. No manual classification, overlay conversion, merge, or execution authorization occurred.

## 5. Exact target software assurance

- Workflow: `.github/workflows/type1-software-assurance-v3.yml`
- Run: `43769702964`
- Job: `132982647007`
- Artifact: `14183497463`
- Artifact SHA-256: `9b8f479e4e6c8f1716da1e0a0f3e24dd36c7a324391e6fc85ae930575788b837`
- Scan commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Review branch commit: `ff71f97a1752f2e998ae740d796eae7dfdc0b9f0`

Scanner results:

- actionlint exit code: 123; 97 diagnostic headers
- zizmor exit code: 14; 205 findings
- zizmor severity: 164 High, 37 Medium, 4 Informational
- Scorecard exit code: 0; score 5.7
- Scorecard reported vulnerabilities: 73

Interpretation: exact target snapshot scanned successfully; findings remain open for path-specific triage and independent review. Workflow conclusion `success` does not mean the security findings passed or were closed.

## 6. Exact current review-branch scan

- Workflow: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Run: `43769805615`
- Job: `132982958386`
- Artifact: `14183542406`
- Artifact SHA-256: `969398affa1b61433f18b869e7e2541a74effd8dae593157abfceb5580ed50f1`
- Intended scan commit: `ff71f97a1752f2e998ae740d796eae7dfdc0b9f0`

The scanner installation step stopped because the workflow invoked `tools/scorecard --version`, which is not supported by the installed Scorecard CLI. Scanner exit codes and report hashes are null. The uploaded artifact is manifest/version evidence only and is not a completed scan.

Required correction: replace the Scorecard version command with `tools/scorecard version`, then rerun the exact-commit workflow against the new review-branch commit containing that correction.

## 7. WDC-SILSO source discrepancy

- Workflow: `.github/workflows/wdc-silso-source-audit-v1.yml`
- Run: `43769935301`
- Job: `132983348244`
- Artifact: `14183339951`
- Current analysis file: `real-data/sunspots_full.csv`
- Current analysis rows: 3328, through 2026-04
- Official source rows: 3334, through 2026-10
- Field mismatches: 4, in 2026-01 through 2026-04
- Newer official rows not appended: 6, in 2026-05 through 2026-10
- Sequence checks: passed
- Analysis file modified: false
- Replication eligibility: false

The local four-month records use provisional markers while the official source uses definitive markers. The discrepancy is retained for explicit data-version and analysis-provenance review. No primary data are changed by this addendum.

## 8. Independent human review

Four independent review requests have been sent:

- Statistical-methods review
- Climate-domain review
- Econometric-domain review
- GitHub Actions / CI security review

No substantive independent review report is recorded by this addendum. An automated out-of-office reply is not a review decision.

## 9. Authority and claim status

The following remain unchanged:

- Protocol freeze: `NOT_FROZEN`
- Formal calibration authorized: `false`
- Confirmatory execution authorized: `false`
- Claim support: `false`
- Promotion authority: `false`
- Human adjudication applied: `false`

## 10. Required next gates

1. Correct the Scorecard version command in the existing exact-commit workflow on the review branch.
2. Run Exact Commit Software Assurance against the new review-branch commit and retain all scanner outputs.
3. Triage findings using exact file/line evidence; do not close findings through generic test success or automated bulk edits.
4. Resolve the WDC-SILSO data-version decision before changing the primary analysis dataset.
5. Obtain and record independent human reviews, including reviewer expertise, conflicts, scope, findings, and explicit decisions.
6. Keep formal calibration, confirmatory execution, protocol freeze, claim support, and promotion unauthorized until their separate evidence and authorization requirements are met.

**Interpretation limit:** This addendum records engineering and provenance evidence only. It does not prove the scientific claim, authorize statistical calibration, establish replication, or grant promotion authority.
