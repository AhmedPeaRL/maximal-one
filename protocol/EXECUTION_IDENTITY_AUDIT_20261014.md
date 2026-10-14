# Execution Identity Audit — 2026-10-14

Status: `CURRENT_RUN_IDENTITY_VERIFIED; HISTORICAL_IDENTITY_DISCREPANCY_OPEN`

Purpose: preserve the identity of one specific GitHub Actions run and prevent artifacts from different runs from being treated as interchangeable.

## Verified run

- Repository: `AhmedPeaRL/maximal-one`
- Workflow: `SOS Robustness Gate`
- Run ID: `38584276226`
- Run URL: https://github.com/AhmedPeaRL/maximal-one/actions/runs/38584276226
- Event: `push` to `main`
- Run head SHA: `e063c1d7b252fbad49ff4255c5ad76b70f9138f9`
- Conclusion: `failure`
- Failed job: `gate`, job ID `115931206330`
- Failed step: `Enforce replication eligibility after evidence collection`
- Recorded reason: `Eligible independent domains: 0/2`; status `REPLICATION_ELIGIBILITY_INSUFFICIENT`.

The run's failure is consistent with the declared replication stop condition. It is not, by itself, evidence of a software defect, secret leak, or scientific falsification.

## Artifact IDs returned for this same run

All IDs below were returned by the GitHub Actions artifact listing for run `38584276226`; the run metadata associates them with head SHA `e063c1d7b252fbad49ff4255c5ad76b70f9138f9`.

| Artifact | Artifact ID |
|---|---:|
| `dataset-eligibility-gate` | `11903944587` |
| `permutation-determinism-audit` | `11904439225` |
| `witness-run-38584276226` | `11905136890` |
| `report-hash` | `11905672175` |
| `final-provenance-closure` | `11905742019` |
| `independent-verification` | `11905996868` |
| `canonical-report` | `11906206825` |
| `reproducibility-manifest` | `11904758644` |
| `external-replay-verification` | `11904813722` |
| `pip-freeze` | `11906345694` |

This record captures artifact identity metadata; it does not assert that each artifact's internal scientific claims are valid. For archival use, download each required artifact and record its downloaded ZIP SHA-256 separately.

## Remaining historical discrepancy

A prior record references commit `6f3430ce9368b956d0c2e35dff1f7bd9c9885ff7`, while the archive's triage record references `3d649a34a6cdf63a05dd8b5aeed03ee4c4d94a5c`. This audit does not establish that those two records describe the same run. Keep the historical discrepancy open until the original run IDs, `GITHUB_SHA`, `git rev-parse HEAD`, and artifact IDs are matched from one source run.

## Output interpretation

- The current run's identity is verified at the run-metadata/artifact-list level.
- The replication gate correctly blocked promotion at `0/2` eligible independent secondary domains.
- `canonical-report` is a run artifact, not a committed file in the repository tree. The `.gitignore` rule for generated `artifacts/` files does not contradict the existence of a downloadable Actions artifact; documentation must not call a runtime artifact “committed” unless a tracked Git blob is independently verified.
- Do not alter claim flags, null thresholds, or scientific inputs to make this run green.
