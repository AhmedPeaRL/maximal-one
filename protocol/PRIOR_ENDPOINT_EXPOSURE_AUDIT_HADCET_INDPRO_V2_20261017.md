# Prior Endpoint Exposure Audit — HadCET and INDPRO — V2

**Record date (UTC):** 2026-10-17  
**Role:** Historical exposure accounting only; not preregistration and not scientific evidence.  
**Claim support:** `false`  
**Promotion authority:** `false`

## 1. Researcher statement retained separately

The researcher previously reported that they had not personally viewed the HadCET and INDPRO endpoint results before completing the relevant preanalysis protocol. This is recorded as a statement about personal inspection only. It is not machine evidence that the endpoint was never computed or displayed.

## 2. Confirmed machine generation and display

The repository's prior audit records the following exact CI event:

- Workflow run: `38729766378`
- Workflow: `SOS Robustness Gate`
- Commit: `3f0ccefbb1304fad1733a91c185c05aa3d619968`
- Job: `core-proof` (`116404370454`)
- Step: `analysis/cross_domain_band_guard.py`
- Observed log timestamp: `2026-10-15T11:50:02Z`
- Logged estimate for `hadcet_monthly.csv`: `0.150544`
- Logged estimate for `fred_indpro_monthly.csv`: `2.530521`
- The recorded implementation used the estimator's default band `0.01 < f < 0.05`.

The evidence supports **computed = YES** and **displayed in CI log = YES** for those endpoint-like estimates. It does **not** establish whether the researcher personally inspected them before a relevant decision. Personal inspection remains `UNKNOWN` unless independently documented.

Run record: https://github.com/AhmedPeaRL/maximal-one/actions/runs/38729766378

## 3. Exposure classification

| Question | HadCET | INDPRO | Evidence status |
|---|---|---|---|
| Was an endpoint-like estimate computed automatically? | YES | YES | Run `38729766378`, step log as recorded above |
| Was the numeric value displayed in a CI log? | YES | YES | Exact values recorded in the historical audit |
| Did the researcher personally inspect the value before the decision? | UNKNOWN | UNKNOWN | The CI log cannot establish personal inspection; retain the researcher statement separately |
| Are these historical values preregistered confirmatory results? | NO | NO | Do not retroactively label outputs confirmatory |
| Is replication approval granted? | NO | NO | Current provenance/independence/null prerequisites remain unresolved |

The values above are preserved as exposure evidence only. Do not use them to choose a transformation, time window, null family, test tail, or candidate eligibility rule. Do not rerun the same historical endpoint and call it fresh confirmation.

## 4. Remaining historical audit work

This audit is **partially complete**, not a claim that every historical workflow/artifact was exhaustively reviewed. Before asserting that the exposure review is complete:

1. Enumerate all historical Actions runs that could have loaded HadCET or INDPRO, not only the known run above.
2. For each matching run, record run ID, workflow path, commit SHA, timestamps, job/step, artifact ID/name, and whether the numeric endpoint appears in logs or artifact contents.
3. Download and hash relevant artifacts when available; do not infer contents from artifact names.
4. Record whether the researcher personally inspected the output as a separate self-report, without inferring it from the machine log.
5. Preserve `UNKNOWN` whenever evidence is unavailable. A failed search or absent artifact is not proof that a computation never occurred.
6. Preserve old logs and outputs. Do not rewrite history or backdate any protocol.

## 5. Decision

- HadCET and INDPRO historical endpoint outputs: `EXPLORATORY_OR_POST_OBSERVATION; NOT_CONFIRMATORY`.
- HadCET and INDPRO replication approval: `NOT_APPROVED`.
- Historical audit completeness: `PARTIAL; ALL_RELEVANT_RUNS_AND_ARTIFACTS_STILL_TO_BE_ENUMERATED`.
- Current independent replication count remains `0/2` unless and until the existing gate reports otherwise on admissible evidence.
- No endpoint calculation for a new candidate is authorized by this file.

## 6. Non-retroactivity rule

Any new confirmatory analysis must use a separately identified dataset or prospectively specified data slice whose endpoint has not been used to select the protocol, after a complete protocol and its data/source identities have been committed. If that condition cannot be established, report the analysis as exploratory/post-observation.
