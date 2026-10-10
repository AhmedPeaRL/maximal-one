# Null Capacity Run Reconciliation — 2026-10-10

## Status

`UNRESOLVED_RUN_SPECIFICATION_DIFFERENCE`

The repository snapshot records a repaired primary-domain capacity audit with:
- selected order: 20
- maximum declared order: 20
- valid surrogate refits: 1000
- boundary fraction: 0.937

The latest workflow log supplied for review reports:
- selected order: 20
- maximum declared order: 20
- boundary fraction: 0.947
- status: CALIBRATION_REQUIRED

The historical pre-repair value was 0.965.

---

## Required handling

Do not silently overwrite one value with another.

First download the artifact from the exact workflow run and compare:
- workflow name and run ID;
- commit SHA;
- script path and script hash;
- dataset hash and sample length;
- surrogate count and seed;
- definition of surrogate_boundary_fraction;
- whether the fraction is calculated from primary-domain refits or synthetic calibration scenarios.

If 0.947 is produced by the same statistic, same dataset, same protocol revision, and same declared run scope as the 0.937 audit, then update the canonical capacity audit and dependent reports together, preserving 0.937 as a prior run result.
If the statistics differ, retain both with distinct names and definitions.

Neither 0.937 nor 0.947 supports or falsifies the hypothesis.
Both indicate boundary saturation above the declared 0.50 review threshold.

The null remains not frozen and claim promotion remains blocked.
