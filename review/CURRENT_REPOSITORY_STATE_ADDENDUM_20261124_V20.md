# HCM Current Repository and Evidence State Addendum — V20

- Evidence date: 2026-11-24
- Repository: `AhmedPeaRL/maximal-one`
- Target branch: `review/type1-v4-remediation`
- Purpose: post-V19 reconciliation of live repository identity and evidence state
- Disposition: `REVIEW_ONLY / MAIN_UNCHANGED / V19_RECORDED / SECURITY_OPEN / CONTAINER_REVIEW_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Independently retrieved repository identity

GitHub comparison confirms:

- Main HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review HEAD: `406300e4c24c452336581ce3f2680b0fb1eda6d3`

Review is exactly at `406300e...` when compared against that commit.

Main remains identical to `9749de9...` in the checked comparison.

## 2. Post-V18 and V19 documentation sequence

The GitHub comparison from `cb8e51a2d915dca9e8bfd5700515afd73e9050e8` to `406300e4c24c452336581ce3f2680b0fb1eda6d3` reports two commits and exactly two changed paths:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261124_V19.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261124_V19.sha256`

The V19 Markdown file is present on Review. Its Git blob SHA is:

`2bf18e978b2dd0a70238ba5cd40b4c7a8556ba10`

The V19 SHA manifest is present and records:

`6fe862b6e3fa2829c9acb297f13fe8d447e3ca7b5063dc599273194c1fe0a460  CURRENT_REPOSITORY_STATE_ADDENDUM_20261124_V19.md`

The V19 text records the pre-V19 baseline `cb8e51a...` and its own insertion as a required next step. It is retained as a historical pre-insertion state record. This V20 addendum supersedes it for the post-insertion current repository identity.

The manifest value above is the value recorded by the repository. A separate owner-side `sha256sum -c` result must be retained as local verification evidence; GitHub presence alone does not establish that local check.

## 3. Fingerprint patch

The Review version of `env/fingerprint.py` remains the hardened implementation retrieved during this audit.

Git blob SHA:

`d337d908e541b6a9ffaa6fec92dd35c261ef1ff8`

The patch uses argv-based subprocess execution with `shell=False`, `sys.executable -m pip freeze`, bounded subprocess timeouts, explicit text encoding, and preserves sorted JSON serialization.

Status remains:

`PATCH_APPLIED / STATIC_REVIEWED / RUNTIME_VALIDATION_PENDING`

No claim of completed runtime or behavioral validation is made.

## 4. Exact-commit assurance workflow

Review workflow path:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Observed blob SHA:

`134fcbfa344c8f7f775f521420709c2886ac288a`

The manual dispatch input is `scan_commit`. The exact target must equal the selected Review branch `GITHUB_SHA`.

The manual `workflow_dispatch` interface does not expose `run_container_review`; that input exists only for `workflow_call`. A manual dispatch of this workflow therefore does not constitute a container build or Trivy image scan.

No new workflow dispatch is authorized by this document.

## 5. Container and Debian status

The previous container review reported 50 HIGH records, 12 unique CVEs, and zero CRITICAL records. The configured Trivy HIGH/CRITICAL policy failed.

The later exact-commit assurance run `45283161110` skipped its container job. It therefore supplied no new image build, CLI smoke, or Trivy result.

As of the 2026-11-24 Debian Security Tracker review, the Trixie source-package status remains vulnerable for the tracked set:

- util-linux: CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410
- SQLite: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379
- systemd: CVE-2026-16742
- OpenSSL: CVE-2026-124709
- acl: CVE-2026-54369
- ncurses: CVE-2025-69720
- Perl: CVE-2026-9538

Exact installed binary package versions in a newly built image still require verification.

Do not suppress findings, mix Forky/Sid packages into Trixie, or edit the Dockerfile before official fix provenance and compatibility are reviewed.

## 6. Reproduction endpoint

The owner attests that `api/public_reproduce_endpoint.py` is not deployed, not connected to a public URL, and not routed through a running service.

Classification:

`REPOSITORY_CODE_PRESENT / OWNER_ATTESTED_NOT_DEPLOYED / NOT_INDEPENDENTLY_VERIFIED`

The retrieved implementation is not a security sandbox. It clones a mutable default branch, has no subprocess timeouts or resource isolation, and does not establish network isolation.

The retrieved `analysis/external_reproduction.py` fetches a fixed public JSON report, does not consume the supplied payload path, and does not create the result file expected by the endpoint.

External payload reproduction is not established. Do not deploy or expose this code without a separate secure execution architecture and independent security review.

## 7. Disabled workflows

The repository owner reconfirms that the following thirteen workflows remain disabled in GitHub settings:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — Main name
6. Build and Publish Container — Review name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress

Classification:

`OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`

The available connector evidence does not independently expose the server-side enabled/disabled state of all thirteen workflows. The owner must visually reconfirm them immediately before any Review push. If uncertain, do not push.

## 8. Independent human review

The four independent reports remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

A bounded Gmail search on 2026-11-24 found no new matching reviewer threads in the searched period. This is not proof that the entire mailbox contains no relevant correspondence.

Acknowledgements, requests, and out-of-office messages do not count as independent review reports.

## 9. Library evidence

The Library contains the exact-commit assurance and OSV artifacts for run `45283161110`.

The stored Review source archive remains historical and does not match Review HEAD `406300e...`. A new archive must be generated from the exact verified post-V20 Review HEAD and stored under a new filename. Preserve older archives as historical records.

## 10. Scientific authority and no-go

The project remains:

- `REVIEW_ONLY`
- `PROTOCOL_NOT_FROZEN`
- `FORMAL_CALIBRATION_NOT_AUTHORIZED`
- `CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`
- `REPLICATION_NOT_AUTHORIZED`
- `CLAIM_SUPPORT_NOT_AUTHORIZED`
- `PROMOTION_NOT_AUTHORIZED`

No new scientific snapshot, Type-I calibration, confirmatory execution, endpoint computation, replication, protocol freeze, publication claim, or promotion is authorized.

Software scanner success is not proof of complete security closure, scientific validity, independent replication, or peer review.

No claim of 100% assurance is made.

## 11. Next-step controls

1. Preserve Main at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
2. Add this V20 Markdown file and its SHA-256 manifest on Review only.
3. Ensure exactly these two V20 paths are changed.
4. Verify the existing V15–V19 SHA manifests locally.
5. Visually reconfirm all thirteen workflows disabled immediately before pushing.
6. Do not edit workflow definitions, Dockerfile, protocol, datasets, or scientific outputs in this documentation step.
7. Do not dispatch any workflow until the exact V20 commit is independently checked and the one permitted Review-only scan target is confirmed.
8. Preserve all prior artifacts and archives without overwriting historical evidence.
