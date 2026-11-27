# HCM Review Patch Manifest — V35

- Target repository: `AhmedPeaRL/maximal-one`
- Required branch: `review/type1-v4-remediation`
- Required base Review HEAD: `c8985c4bfcb6140dbfd081a4eb2faab29fb561af`
- Main must remain: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Proposed commit SHA: `PENDING — not committed`
- Authorization: `NOT AUTHORIZED TO COMMIT UNTIL FRESH GET-ONLY WORKFLOW STATE CHECK`
- Workflow authorization: `NONE IN THIS ROUND`

## File manifest

| Operation | Repository path | Base Git blob SHA-1 | New Git blob SHA-1 | New content SHA-256 | Reason |
|---|---|---|---|---|---|
| Replace | `tools/hcm_readonly_github_audit.sh` | `280e8f8790a892a058ef13718ce1e63eadc0dea9` | `4d8eeaa2cd0a5cd66cc02906652606868501aa1a` | `98102a9deffe57f529aa5612eb5aae30f864d554392bdff44c69ce296907e106` | Encode Review branch path; capture Review head/protection; query orphan and known workflow IDs; capture all/Main/Review run histories; timestamp the snapshot and hash every output; retain GET-only behavior. |
| Replace | `tests/test_hcm_readonly_github_audit.py` | `f19dc5666c093eb6cfb8aff389b9bf1732be60b6` | `6409109a8b8a38b1970b657aee7afc535744e00a` | `5ccd694069b18f75ed48b9a65807a1d4553cd3f0fbff39d15930955b890d254a` | Add static regression coverage for encoded branch paths, branch protection, direct ID reads, run histories, timestamp/hash outputs, GET-only calls, no mutation/dispatch, and token-safe authentication. |
| Add | `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261127_V35.md` | — | `f04e5844b7966b90630b2823772d8d53e706cb91` | `c47c95d66293a52a5a38040a8d6748b9270dbb7345853a4d4dbbb4c4faf36653` | Current state, workflow audit, Run 48 artifacts, container/CVE/science/hosting status, patch rationale, tests, and closure criteria. |
| Add | `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261127_V35.md.sha256` | — | `260ca49b8c42eadf43b0c907a8132a0bd70f9e88` | `3e8807831cb2cff12659fef613f211a789eff02a4645b416ca6c83d13166defd` | Companion integrity check for the V35 addendum. |
| Add | `docs/DEBIAN_TRIXIE_CVE_STATUS_20261127.md` | — | `97475ad14a02d90ed7b84084bc22dab4252d804f` | `2412e8cf4b61a6ac970da853086946cf2481c67e6f8eab8b58c430e0a59702ab` | Current Debian Trixie tracker status for historical CVEs; explicitly not a current image inventory. |
| Add | `docs/HCM_SECURITY_TRIAGE_REGISTER_V2.csv` | — | `baac403fd070384fd41cfb9129ba2ea8648df498` | `e4236c1df4aaecb641c8385d3009263ca3caeb273b300bc77d181fa4e36b983d` | Current risks, evidence, closure criteria, and owner actions. |
| Add | `docs/HCM_WORKFLOW_EXECUTION_POLICY_V2.md` | — | `25d05b3e69e5c09e657261008d45cb7c52603c08` | `227a20e28e5e54f32077fa3401c8dcf3f621a7d40d4ab31ae145515f94ef83d0` | Main freeze, no-run rule, Review push guard, and only future candidate. |

## Existing files intentionally preserved

- `docs/HCM_WORKFLOW_EXECUTION_POLICY_V1.md` blob `bb0d28a7e398514f206ab504b9f157efd597162f` — preserved, not overwritten.
- `docs/DEBIAN_TRIXIE_CVE_STATUS_20261124.md` blob `b97a3165533446a96177133b9bc8c7e57702bfc1` — preserved, not overwritten.
- `docs/HCM_SECURITY_TRIAGE_REGISTER_V1.csv` blob `8137196ecdeb63b2eb58619d1495a6d974869020` — preserved, not overwritten.
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261124_V22.md` blob `9405bda5464a1e449825f3b66717c953fe9266ae` — preserved as historical evidence, not overwritten.
- `.gitignore` blob `b3452494cacd07bd3a286ac5bf7c76f2aaf12866`, `.dockerignore` blob `30d7f19176daca8001d3e82d3b1e3944be57a839`, and `Dockerfile` blob `fe8dd29e9ef30a58d795e33d903b250ddf12b4e8` — unchanged by this patch.

## Local tests performed

- `bash -n tools/hcm_readonly_github_audit.sh`: PASS.
- `python -m unittest discover -s tests -v`: 10 tests PASS.
- Mocked GET-only CLI smoke test: PASS; all generated output checksums verified.
- CSV validation: 13 data rows, 7 columns: PASS.
- ShellCheck: not installed in the preparation environment; no pass claimed.
- No network call was made by these local tests.

## Closure and authorization

The patch is prepared, not committed. Before any push, a fresh authenticated Termux GET-only audit must confirm `.github/workflows/build-image.yml` remains `disabled_manually`, reconcile the full workflow ID/path/state inventory, and preserve both branch protection responses and API error states. If the state is active, unavailable, or ambiguous, do not commit.

After a permitted Review-only commit, verify the exact new Review HEAD and every changed blob SHA. Do not run a workflow automatically. The only future candidate to consider after separate explicit approval is `.github/workflows/software-assurance-exact-commit-v1.yml` on Review with `scan_commit` equal to the exact full Review HEAD. No workflow is authorized now.
