# Type-I Calibration Artifact Register — 2026-10-11

Source of identity metadata: GitHub Actions run `38088677966`, workflow `.github/workflows/null-type1-calibration.yml`, branch `main`, commit `179c2bb01167ed9f3d3deda6549c2b893faeabb5`. GitHub reported all four artifacts unexpired with expiry `2027-01-08T21:42:57Z` at the time reviewed.

## Artifacts

| Scenario | Artifact ID | ZIP SHA-256 | Rejections / 1000 | Rate | Wilson 95% interval | Status |
|---|---:|---|---:|---:|---|---|
| AR(1), phi=0.4 | 11687241416 | `22bb2816695e4b199917ea6f02585f4b912f7f5266cef39dcefb749e008c5d2b` | 52 | 0.052 | [0.039873, 0.067556] | Pass, limited synthetic scope |
| AR(5), low-order coefficients | 11687017681 | `d4b23c028180dda510573de8c65db14ac89a0b3251f928a3a1707370a78e714b` | 49 | 0.049 | [0.037261, 0.064191] | Pass, limited synthetic scope |
| AR(2), phi=(0.45,-0.10) | 11687415527 | `850b8399f0f949a92f8f06d2d19d9808d8ee7357ef4c5b119943c37c9b936723` | 60 | 0.060 | [0.046896, 0.076471] | Fail current criterion |
| AR(10), low-order coefficients | 11685850751 | `4c332df61577dc53269a1a1da08f0a472de67b463edde013ba47efddc3080f20` | 73 | 0.073 | [0.058459, 0.090809] | Fail current criterion |

## Immutable artifact URLs

- AR(1): https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11687241416
- AR(5): https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11687017681
- AR(2): https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11687415527
- AR(10): https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11685850751

## Verified provenance

GitHub's artifact listing tied each artifact to run `38088677966`, branch `main`, and head SHA `179c2bb01167ed9f3d3deda6549c2b893faeabb5`. The review downloaded all four ZIPs and inspected the JSON members. The ZIP digest values above are the SHA-256 values of the downloaded ZIP bytes and match the artifact-upload digests recorded by GitHub in the logs.

Each artifact explicitly records `claim_support: false`, `promotion_authority: false`, and `confirmatory_null_frozen: false`. Preserve these records as evidence; do not replace failures with later passes or treat a synthetic pass as claim promotion.

The `requirements-lock.txt` hash-coverage concern remains separate and unresolved by this register. This package does not rewrite that lock file because the full transitive dependency closure and intended platform targets must be verified against the repository's declared installation method first.
