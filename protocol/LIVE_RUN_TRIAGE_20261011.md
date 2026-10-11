# Live Run Triage — 2026-10-11

## 1. Current decision

The live scientific gate is correctly withholding claim promotion. The supplied run reports:

- claim status: `UNDER_INVESTIGATION`
- claim support: `false`
- primary stochastic null rejected: `false`
- primary stochastic-null p-value: `0.999001`
- clean-checkout computational reproducibility: `true`
- adversarial control: `true`
- final promotion allowed: `false`
- eligible independent secondary replication domains: `0/2`

The p-value is not evidence supporting the stated alternative. Computational reproducibility and an adversarial-control pass do not override the null result or missing independent replication.

## 2. Why the two workflows fail

The `scientific-claim-promotion.yml` eligibility gate exits nonzero because it found `0/2` eligible independent replication domains. The `scientific-validation.yml` consensus step exits nonzero because `replication_eligible_real_domains` is zero and `independent_real_domain_evaluation_complete` is false. These are expected fail-closed outcomes under the currently declared claim contract, not proof that the software itself is broken.

The log shows two measurement-valid secondary series (CO2 and cosmic rays), but neither currently qualifies for replication:

- CO2: 816 rows, below the declared 1024-sample replication minimum; provenance fields are also incomplete.
- Cosmic rays: 3698 rows, but timestamps/cadence/gaps and source provenance have not passed the required review. The reported 321 gaps and longest exact hourly run of 486 observations mean a plain row-count check cannot establish a valid canonical regularly sampled series.
- Airline passengers (144), global temperature (146), and S&P 500 (252) are below the declared measurement minimum of 256 or estimator/replication requirements as reported by the gate. They must not be padded or admitted by lowering the threshold after inspecting results.
- `sunspots_full.csv` is the primary domain and must not count as a secondary independent replication domain. `sunspots_global_extended.csv` is derived from it and must not count either.

## 3. Preserve the distinction between three states

1. **Measurement-valid:** the declared estimator can be computed under the structural rules.
2. **Replication-eligible:** structural requirements and provenance/independence requirements are satisfied.
3. **Scientific replication established:** the eligible independent domain rejects the same predeclared null family, endpoint, direction, and tail under the required protocol.

The current run reaches neither replication eligibility nor scientific replication for two secondary domains.

## 4. Required next actions

1. Preserve the exact workflow run IDs, commit SHA, generated JSON artifacts, and Type-I scenario artifacts before any change.
2. Resolve the primary AR(p) null-capacity review. The `937/1000` versus `947/1000` boundary fraction discrepancy must be reconciled to exact run IDs, commits, data/code hashes, seed, and surrogate definition. Do not choose one by preference.
3. Complete a prospective, scientifically justified null-adequacy protocol before confirmatory reanalysis. The current AR(p) protocol is marked exploratory/post-observation and not frozen.
4. Predeclare the INDPRO transformation (raw, log, difference, or detrended residual) and the HadCET window/precision policy before inspecting endpoint alpha for confirmatory use. Record prior exposure honestly.
5. For cosmic rays, retain original timestamps through the audit and establish cadence, missingness, longest contiguous run, source identity, and shared solar-cycle nuisance handling before reconsidering eligibility.
6. Only after those reviews, run the declared domain-level null test on the same endpoint and null family. Keep the promotion gate blocked until all criteria pass.

## 5. Do not do

- Do not mark `replication_eligible` or provenance approval true merely to clear CI.
- Do not lower the 1024 replication minimum or adapt `nperseg` to admit short series after observing outcomes.
- Do not replace the primary null with permutation or a more favorable null after observing the p-value.
- Do not average different Type-I scenarios to hide a failed scenario unless a scientifically justified aggregate rule was specified prospectively.
- Do not describe this repository as unhackable, a validated market/space/banking infrastructure, or evidence of HCM causation based on these logs.
