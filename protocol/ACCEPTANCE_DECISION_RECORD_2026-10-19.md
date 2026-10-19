# Acceptance Decision Record — 2026-10-19

**Decision ID:** `HCM-NULL-CALIBRATION-HOLD-2026-10-19`  
**Reviewed commit SHA:** `9fcd54bbc56ccf4c13b7b2020aa5f02b5f2b7ce5`  
**Calibration run:** [39155162528](https://github.com/AhmedPeaRL/maximal-one/actions/runs/39155162528)  
**Raw audit run:** [39155206532](https://github.com/AhmedPeaRL/maximal-one/actions/runs/39155206532)  
**Claim-promotion run:** [39155182272](https://github.com/AhmedPeaRL/maximal-one/actions/runs/39155182272)  
**Protocol/matrix SHA-256:** `PENDING_AFTER_COMMIT`  
**Independent reviewer identity/expertise and dated decision:** `PENDING — NOT SUPPLIED`  
**Claim support / promotion authority / confirmatory endpoint authorization:** `false`

## Criteria

| Criterion | Status | Evidence / rationale |
|---|---|---|
| Exact checkout identity for historical calibration jobs | PASS | Four jobs recorded the reviewed commit. |
| Historical results preserved | PASS | Four scenario artifacts exist in run 39155162528. |
| Historical Type-I rule passes all four scenarios | FAIL | AR(2) and AR(10) fail the committed rule. |
| Calibration configuration equals production | FAIL | Calibration requests 200 surrogates; production requests 1000. |
| Expanded scenario matrix frozen and independently approved | NOT_ASSESSED | Draft only; review pending. |
| Power study/alternative generator validated | NOT_ASSESSED | Not run; blocked pending Type-I equivalence and review. |
| Empirical reference hashes and independent approval complete | NOT_ASSESSED | Registry template remains unregistered; no approval is asserted. |
| Raw candidate audit passed | FAIL | Run 39155206532 reports structural/missingness block. |
| At least two independent secondary domains eligible | FAIL | Run 39155182272 reports 0/2. |
| Attributable independent statistical review recorded | NOT_ASSESSED | Reviewer identity and signed decision are pending. |

## Recorded outcomes

- AR(1): 52/1000, rate 0.052, Wilson interval [0.039873, 0.067556], pass under historical rule only.
- AR(2): 60/1000, rate 0.060, interval [0.046896, 0.076471], fail: upper endpoint > 0.075.
- AR(5): 49/1000, rate 0.049, interval [0.037261, 0.064191], pass under historical rule only.
- AR(10): 73/1000, rate 0.073, interval [0.058459, 0.090809], fail: interval excludes 0.05 and upper endpoint > 0.075.

These results are for the 200-surrogate calibration configuration and are not exact calibration of production's 1000-surrogate setting.

## Final disposition

**Decision:** `HOLD_INCOMPLETE_EVIDENCE`  
**Freeze state:** `NOT_FROZEN`  
**Confirmatory endpoint authorization:** `false`  
**Claim promotion:** `NOT_APPROVED`

Reason: two historical scenarios fail; calibration and production surrogate counts differ; raw audit is blocked; eligible independent secondary domains are 0/2; reference registration and independent review remain incomplete.

**Reviewer statement:** `PENDING — no independent reviewer has signed or otherwise recorded approval.`

This draft is not a signature or approval on behalf of an independent statistician.
