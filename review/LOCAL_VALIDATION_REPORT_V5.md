# Local validation report — V5 current-source refresh

Date: 2026-11-12. This report covers local validation only; the new GitHub workflows have not yet been committed or executed.

## Passed locally

- All 10 existing `tests.test_type1_target_batch_generation_v3` unit tests passed.
- The unchanged V3 batch generator was run against the downloaded latest inventory artifact `13975650287` and the new V4 population register. It generated 72 batch JSON files, 25 IDs each, 1,800 total IDs, 1,800 unique IDs, all source-bound to inventory run `43285928305`, target ledger SHA `10c45fcaaec47819dc59df75d6f28a801022d185187933f10c665d858016b5e8`, main commit `982c6a10f1bd4262a9915f40a3c821adfd5c58c2`, and main ledger SHA `6b2e8955256418c1db3d3084e889c9d284ba463fd8fadd3e3e7d08f2bc274c9d`.
- The three V4 CSV occurrence IDs exist in the latest 1,800-record target ledger. All three remain OPEN/PENDING; reviewer and classification fields are blank; second review is PENDING; no adjudication was applied.
- Inventory and snapshot artifacts passed ZIP integrity checks. Inventory SHA register and all source ledger/provenance checksums were verified. Snapshot has 289/289 files and 292 successful extraction checks.
- All three new workflow YAML files parsed successfully with PyYAML.
- Package JSON files parsed; CSV hash matches the population register; ZIP integrity passed; package file checksums verified.

## Not performed / not claimed

- `actionlint` and `zizmor` are not installed in this local execution environment, so the three new workflow files were not linted with those tools here. GitHub Actions must run them after upload; no clean-lint claim is made.
- The new Batch V4, Preflight V5, and Software Assurance V3 workflows have not been committed or executed on GitHub.
- No GitHub commit was created by this assistant.
- Local generation is not a GitHub artifact and is not an independent review.
