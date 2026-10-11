# Type-I Acceptance Operating Characteristics — Interpretation

The committed audit describes the current acceptance rule: with 1000 repetitions and a nominal rejection probability of 0.05, accept a scenario only when its two-sided 95% Wilson upper confidence endpoint is at most 0.075. The audit is explicitly marked `audit_only=true` and `production_gate_modified=false`.

## Reported calculations

- Accepted rejection counts: 0 through 58 inclusive.
- Wilson upper endpoint at 58/1000: approximately 0.0742496.
- Wilson upper endpoint at 59/1000: approximately 0.0753609, above the 0.075 cutoff.
- Under the binomial model with p=0.05, one nominal scenario passes with probability about 0.88944 and falsely fails with probability about 0.11056.
- If four scenarios were independent and all had p=0.05, the probability all four pass would be about 0.62584; the probability at least one falsely fails would be about 0.37416.

## Critical qualification

The four-scenario family calculation is conditional on the audit's explicit independence assumption. The scenario outcomes should not be treated as independent merely because they are separately named. Therefore, `0.37416` is a model-based illustration under the stated assumption, not an established empirical family-wise error rate for the actual scenarios.

The stricter scenario rule may be intentionally conservative, but it has a nontrivial false-failure probability under the nominal binomial model. That is a design trade-off to document and review prospectively, not a reason to weaken the gate after seeing failures.

## Interpretation alongside the live scenario runs

AR(1) and AR(5) passed only their named synthetic scenarios. AR(2) and AR(10) failed the declared acceptance criterion. AR(2)'s Wilson interval includes 0.05, but its upper endpoint exceeds 0.075; AR(10)'s interval excludes 0.05 and its upper endpoint exceeds 0.075. These outcomes must remain separate. Passing two scenarios does not cancel the two failures, and none of these synthetic scenarios by itself establishes that the null is adequate for the real sunspot series.

## Required handling

Preserve each scenario's artifact, commit, code/data hashes, seed, model specification, rejection count, and interval. Any revised acceptance rule must be justified and frozen prospectively before new confirmatory runs. Do not repeatedly rerun until a favorable outcome appears.
