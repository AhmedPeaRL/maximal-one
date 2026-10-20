# Type-I Calibration V3 Review Decision Record — V1

**Disposition:** `HOLD_NOT_FROZEN`
**Applies to snapshot:** `d72d82b22322ecc2b771c5b41b47379782098823`
**Purpose:** record decisions that must be resolved before any formal calibration run.

## Findings established from the repository snapshot

1. The V3 candidate matrix uses `n=1024`, while the primary real series is reported as `n=3328`. With `nperseg=1024`, this changes Welch averaging from approximately five overlapping segments in the longer series to one segment in the calibration series. This is a material operating-characteristic mismatch.
2. The two V3 complex-root AR(2) scenarios use angular frequency `theta=pi/3`, corresponding to `f=theta/(2*pi)=1/6`, outside the tested open band `(0.01, 0.05)`. They test persistence/resonance outside the target band, not a peak inside it.
3. The inherited ceiling `0.075` does not by itself establish calibration at nominal `0.05`. It permits a Type-I rate up to 50% above nominal. No consequence-based justification is currently recorded, so the ceiling is **unresolved**, not approved.
4. The current candidate runner records checkpoints but does not reload them, does not implement replicate-range sharding/merge, and does not establish runtime feasibility for the proposed 18,000,000 surrogate requests.
5. The current workflow's prepare step blocks unless the matrix is explicitly `APPROVED_FROZEN`, `FROZEN`, authorized, and archive identity verified. Keep that block intact until the evidence and independent review exist.
6. The current run `39341038316` is the **Claim Promotion Gate**, not the Type-I calibration workflow. Its failure is not evidence that the Type-I pilot ran.

## Decisions for the next evidence-gathering phase

- Keep V3 unchanged as a historical candidate. Do not relabel its historical outputs.
- Create V4 only as a **draft for review**: use the production series length (`n=3328`) for the primary synthetic scenarios and include in-band resonant AR(2) stress scenarios. Do not treat this matrix as frozen.
- Do not claim that `0.075` is justified. An attributable statistician must either provide a decision-consequence rationale and approve it, or specify a different prospective rule before formal simulation.
- Keep the current conservative invalid-attempt policy for the pilot: preserve every attempt; an invalid attempt makes that pilot diagnostic inconclusive; do not silently drop, replace, or relabel invalid attempts. The formal policy must be approved by the human reviewer before freeze.
- Run only the separate exploratory pilot workflow in this package. Its outputs are for runtime, failure-mode, determinism, and resume/shard engineering diagnostics—not a Type-I pass and not confirmatory evidence.
- Add the production-equivalence golden test to the formal gate only after the exact production preprocessing path is exposed and compared on the same synthetic input. A test of constants alone is insufficient.
- Do not edit `core-scientific/strict_claim.json`, promotion flags, historical results, or the production null implementation as part of this package.

## Freeze checklist (all required)

- [ ] Named, attributable independent human statistician has reviewed and signed the estimand, scenario matrix, threshold rationale, invalid policy, and computational plan.
- [ ] V4 scenarios are finalized prospectively; all primary scenarios use production-matched sample length and in-band resonance is represented.
- [ ] The `0.075` criterion is justified by decision consequences or replaced before data collection; its operating characteristics are simulated/reported.
- [ ] Production preprocessing and calibration path pass a golden behavioral equivalence test on identical series and seed.
- [ ] Pilot has measured runtime and documented invalid/failure patterns.
- [ ] Sharding, deterministic merge, checkpoint resume, and interrupted-run behavior pass automated tests.
- [ ] Clean archive/repository identity, commit SHA, dependency lock hash, matrix hash, master seed, stable scenario IDs, and run IDs are recorded.
- [ ] Only then: reviewer approval and a new freeze commit; formal calibration may be dispatched afterward.

**No item in this record authorizes formal calibration, power analysis, production-null freeze, or scientific claim promotion.**
