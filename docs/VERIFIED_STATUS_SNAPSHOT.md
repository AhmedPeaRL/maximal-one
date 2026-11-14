# Verified status snapshot — 2026-11-14

| Item | Evidence-based status |
|---|---|
| Review commit | `1229ce760055de83fc07f77c050a59ce0a26eeb5` |
| Main at compare time | `160acfc8600b66c7300f2fd0caa500972de740b8` |
| Compare | diverged; review commit 467 ahead / 34 behind |
| New build job | SUCCESS; local image only |
| New stability job | FAILURE at dependency build; no scientific tests executed |
| New publish job | SKIPPED |
| New run artifacts | none |
| Prior review-branch GHCR push | SUCCESS; pushed `latest` |
| Prior published digest | `sha256:5c930ed151cbba762d66ec2d0fc6e4de02637b6bc41455276e29069824899c96` |
| Prior SHA-specific image tag | not observed in prior push log; only `latest` was pushed |
| Current GHCR package version list | not yet queried through authenticated Packages API |
| Payload-to-shell interpolation | still present at lines 1510, 1529, 3290, 3294 |
| Workflow-wide permissions | still broad in scientific-validation.yml |
| Workflow-wide secrets | still present |
| release-lock workflow_run upstream | referenced name not found in inspected snapshots; unresolved/dormant |
| Previous unpinned action findings | 151; require fresh scan after remediation |
| Professor Machiry reply | no reply found in the searched Gmail thread; sent request only |
| Statistical authorization | unchanged; no formal calibration/confirmatory authorization implied |

## Decision

Do not merge the review branch into main. Do not run formal calibration or claim-promotion work on the basis of these security changes. Treat the new workflow as a partial engineering improvement with a failing stability prerequisite and unresolved P0/P1 security work.
