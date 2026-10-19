# Secondary-Domain Review Status — 2026-10-20

**Claim support:** `false`  
**Promotion authority:** `false`  
**Independent eligible replication domains:** `0/2` unless a later admissible gate artifact proves otherwise.

## HadCET and INDPRO

The attached V2 prior-endpoint exposure audit records that endpoint-like estimates for both `hadcet_monthly.csv` and `fred_indpro_monthly.csv` were computed and displayed in a historical CI log (run `38729766378`, commit `3f0ccefbb1304fad1733a91c185c05aa3d619968`). Whether the researcher personally inspected those values before the relevant decision remains `UNKNOWN`; it must not be inferred from the CI log. Those historical values are exploratory/post-observation and are not confirmatory evidence.

Current disposition for both datasets remains `NOT_APPROVED_FOR_INDEPENDENT_REPLICATION`. Their measurement validity does not establish source independence, endpoint non-exposure, suitable confirmatory-null adequacy, or independent-domain replication. The historical exposure audit is marked partial because all relevant Actions runs/artifacts have not been exhaustively enumerated and hashed.

Before reconsideration, preserve the existing audit and separately record, for every relevant historical run, run ID, workflow path, commit, timestamp, job/step, artifact ID/name, and evidence of endpoint computation/display. Keep personal inspection status separate and `UNKNOWN` unless independently documented. Do not backdate or retroactively relabel outputs as confirmatory.

For any future confirmatory use, require a newly identified data slice/source identity not used to select the protocol, frozen endpoint and null protocol, verified provenance/checksum/license/cadence, source independence, common-nuisance review, and the same predeclared eligibility rules. If prior exposure cannot be ruled out for a proposed endpoint, classify it as exploratory/post-observation rather than manufacture a clean confirmation.

## Cosmic rays

`real-data/cosmic_rays.csv` remains `BLOCKED_NOT_REPLICATION_ELIGIBLE`. The supplied audit reports 3,698 timestamped rows but 321 non-hourly intervals, longest uninterrupted hourly run 486, missing provenance fields, and a cleaned value-only pipeline input that drops timestamps. The dataset also needs a documented common-nuisance review against the solar-cycle structure of the primary sunspot domain.

Do not interpolate, silently remove gaps, concatenate disjoint segments, or relax the minimum sample requirement to make this dataset pass. Reconsider only after original-source identification, checksum/license verification, timestamp-preserving input, cadence/continuity audit, a qualifying uninterrupted segment under the already-declared rule, and common-nuisance review. Until all gates pass, it receives zero replication credit.
