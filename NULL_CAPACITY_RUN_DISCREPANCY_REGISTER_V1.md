# Null Capacity Run Discrepancy Register V1

## Status

- Scientific claim: `UNDER_INVESTIGATION`.
- Confirmatory null: `NOT_FROZEN`.
- Claim and promotion authority: `NONE`.
- This register documents inconsistent reported diagnostics; it does not select a preferred result.

## Reported values that must remain distinct until reconciled

| Reported value | Evidence currently available | Interpretation |
|---|---|---|
| `0.937` | `core-scientific/strict_claim.json` records 937 of 1000 valid surrogate refits at AR order 20 in the repaired capacity review. | Historical run-specific result; not automatically the latest run. |
| `0.947` | The supplied `scientific-claim-promotion.yml` log for GitHub Actions run `38040221517` prints selected order 20, maximum order 20, and surrogate boundary fraction `0.947`. | Latest supplied gate diagnostic; underlying run artifact and exact commit must be linked before replacing any registry value. |
| `0.965` | Mentioned in earlier public report material as an older result. | Historical only; verify its run, script, data, and protocol hashes before citing as current. |

## Required reconciliation record

For each value, preserve or retrieve:

1. Git commit SHA and workflow run ID.
2. Exact artifact file and SHA-256 digest.
3. Dataset snapshot SHA-256 and row count.
4. Null implementation and protocol ID/version.
5. Random seed, valid refit count, failed refit count, and denominator definition.
6. Exact calculation of `surrogate_boundary_fraction` and the order-selection comparison/holdback implementation.
7. Python/dependency versions and runner image.

Do not average these values, overwrite the older record, or change the boundary threshold to make the gate pass. If the underlying artifacts cannot be retrieved, mark the value `unreconciled` rather than guessing.

## Decision rule

Boundary saturation remains a model-capacity warning. The reported `0.947` exceeds the declared `0.50` review threshold, so the current AR(p) null remains non-confirmatory. This discrepancy register does not approve a different AR order, a different null family, or a confirmatory analysis. Any future null change requires a dated prospective protocol amendment and fresh validation; observed candidate alpha must not be used to choose the null.
