# Independent audit findings — supplied GitHub runs and artifacts

## Scope inspected

Repository: `AhmedPeaRL/maximal-one`
Target: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
Review head: `4d0fe317ff8e20cdd7f1767e31215d958d87508b`
Main head at the latest inventory run: `0fa531bc844b1891f0574564add8eef5e20813d8`

Inspected the supplied commit and branch refs, workflow run metadata, job steps/logs, artifact inventories, and downloaded ZIP contents for the supplied artifact IDs. The current target inventory and exact-target snapshot were independently checked locally from their downloaded artifacts.

## Source identity

The newest inventory run `42870936071` produced artifact `13789382482`. Its provenance pins target `ad106...`, main `0fa531...`, workflow definition `4d0fe...`, and inventory SHA `b30db3...`. Its target ledger contains 1,800 occurrences and hashes to `fcbc907...`; its main ledger contains 711 occurrences and hashes to `9801d4...`. Both reconciliation records report `RECONCILED`, exact counts, and no missing or extra IDs.

The newest exact-target snapshot run `42871210051` produced artifact `13788334234`. Its three-way certificate binds the same target and inventory SHA. It reports 289 selected / 289 present files, no missing scope or required paths, and zero pre-existing overlay records. The inner self-contained ZIP hash is `332fa4...`; its extraction verification reports 292 checked files and no errors. The downloaded ZIP's inner `SHA256SUMS.txt` verifies the extracted payload.

The earlier population register V1 used a different main comparison commit `484b6...`, 697 main occurrences, inventory SHA `beb593...`, and target ledger SHA `ad8d93...`. Those values are not the latest current-main comparison. The current register must be V2, not a silent mutation of V1.

## Overlay apply failure

Run `42872743465`, job `130027966057`, failed in step `Verify inventory, snapshot, and population identities`. The inventory and snapshot download steps completed. The checksum step executed `sha256sum -c SHA256SUMS.txt` in the outer snapshot artifact directory. That outer artifact contains the checksum file, manifest, certificate, extraction verification, and the nested `self-contained-review-snapshot.zip`; it does not contain the 289 repository files at the paths named in the outer checksum list. Those files are in the nested ZIP. The resulting `No such file or directory` messages are therefore explained by a packaging-level verification-root error.

CSV conversion, schema validation, merge, untouched-record verification, and artifact upload were skipped. The run produced no output artifact. The proper fix is to verify the inner ZIP hash against the certificate, extract the inner ZIP, and run its own checksum list from the extracted root. The V2 workflow implements that sequence.

## Manual adjudication tests

Commit `4d0fe...` adds the file `PATCHES/test_type1_manual_adjudication_overlay_v3_additions.patch` (58 lines), but the actual `tests/test_type1_manual_adjudication_overlay_v3.py` at that commit does not contain the three new regression tests. The governance test run `42870523334` ran 31 existing tests and passed; it did not exercise those not-yet-applied tests. The merger script already contains the overwrite guard. Apply the patch to the actual test module and rerun it; do not treat the patch file's presence as test evidence.

## Batch register

Batch run `42870617536`, artifact `13790040735`, passed its workflow, but its batch records pin inventory SHA `88222e...` and source ledger SHA `5aaa4a...`. The generator and workflow also hardcode those old values. This does not match the newest inventory `b30db3...` and target ledger `fcbc90...`. The batch artifact is therefore stale for the current population. Regenerate using the V2 script and current inventory artifact.

## Engineering runs

- `42870576974`: 24 tests passed; the log states that no standalone runtime-pilot or cross-runner workflow was dispatched in that run. Its uploaded artifact `13789592172` records 23 identity-field mismatch cases rejected with checkpoint and manifest hashes unchanged.
- `42870664509`: the downloaded artifact `13789830986` contains 18 source files (plus snapshot metadata and an inner ZIP). It is a governance-implementation subset snapshot, not the 289-file exact-target snapshot from run `42871210051`.
- `42870135490`: two valid pilot attempts, 200 surrogates each; p-values `0.1890547` and `0.0248756`; explicitly diagnostic-only.
- `42870239737`: all six worker replicates matched the connected reference; each used 1,000 surrogates. I downloaded all six worker artifacts plus the connected-reference and comparison artifacts. Each worker artifact contains exactly one valid replicate, no missing indices, and zero invalid attempts. The six worker `runner_instance_id` values are distinct, and each worker attempt record exactly equals its corresponding connected-reference record. All seven platform identities (reference plus six workers) are nevertheless `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`; this supports repeatability across separate hosted runner instances on the same platform, not cross-platform replication.
- `42870298995`: assignment matrix audit `PASS_ENGINEERING_ONLY`; matrices A and B covered indices 0–5, no mismatches, 1,000 surrogates per replicate.
- `42870347767`: full-path engineering equivalence passed with six completed replicate indices, no missing indices, no invalid attempts, and 1,000 surrogates per replicate. Its evidence summary explicitly says formal calibration is false.
- `42870440350`: failed in `test_direct_entrypoint_rejects_non_actions_context_even_on_review_ref` because the test expected `requires GitHub Actions context` while the implementation emitted `requires the GitHub Actions execution context`. The guard did reject the unauthorized invocation; however, the test suite stopped there and later official-runner equivalence tests were skipped. Correct the assertion and rerun.
- `42870198624`: the CLI resume report lists 19 identity fields; every mismatch was rejected and both checkpoint and manifest remained unchanged.
- `42870576974` artifact `13789592172`: a separate 23-identity-field mismatch suite was rejected; before/after checkpoint and manifest hashes were equal in every case.

These are software-integrity and engineering-equivalence findings only. They do not establish the Type-I error rate or a formal calibration pass.

## Branch divergence

The repository default branch is `main`. GitHub's compare endpoint reports the review branch as 390 commits ahead and 24 behind main, with a diverged status. Do not merge the review branch wholesale. If a manually dispatched workflow must be available, add the new workflow file to `main` and to the review branch as an isolated workflow-only change; run it with the selected ref set to the review branch. Keep the workflow permissions read-only and artifact-only.

## Decision

1. Use the V2 population register and V2 CSV; preserve V1 as historical.
2. Apply and run the missing overwrite regression tests.
3. Correct the branch-guard test regex and rerun the failed engineering workflow.
4. Regenerate batches against inventory `b30db3...` / target ledger `fcbc90...`.
5. Repair snapshot verification by extracting and verifying the inner archive.
6. Do not enter adjudications until a human reviewer actually examines each occurrence. High-impact decisions require a distinct second human reviewer.
7. Keep all authority flags false and protocol freeze NOT_FROZEN.
