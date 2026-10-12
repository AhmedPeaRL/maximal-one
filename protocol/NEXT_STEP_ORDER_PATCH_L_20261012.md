# Next-Step Order — Patch L (2026-10-12)

This patch records the researcher's statement about prior viewing; it does not alter scientific calculations, eligibility gates, workflow logic, or the claim status.

## Required order

1. Commit `PRIOR_ENDPOINT_EXPOSURE_STATEMENT_HADCET_INDPRO_20261012.md` as an audit note. Do not claim this note itself is preregistration.
2. Review historical Actions runs and artifacts for HadCET/INDPRO endpoint outputs. Record run IDs, commit SHAs, generation timestamps, and whether values were actually inspected.
3. Complete `SECONDARY_DOMAIN_PREANALYSIS_DECISION_TEMPLATE_V1.md` with exact, code-grounded estimator settings and prospective scientific choices. Do not leave `TO_BE_COMPLETED` fields in a document described as finalized.
4. Commit the completed protocol before computing or inspecting the two endpoint results.
5. Only then run one candidate at a time under the frozen protocol. Keep failed eligibility, provenance, independence, and null-calibration checks as failures; do not loosen thresholds post hoc.
6. Treat any protocol amendment made after outputs are generated or inspected as an amendment, with date, rationale, and exploratory/post-observation classification where applicable.

## No changes made to

- canonical report or scientific inputs;
- dataset eligibility decisions;
- stochastic-null or permutation-null gates;
- AR maximum order or calibration thresholds;
- claim-support or promotion authority.
