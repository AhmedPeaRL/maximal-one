# Linked evidence index

All run and artifact IDs below were checked against the supplied repository context. Artifact ZIPs listed here were downloaded and inspected, including all eight artifacts from run `42870239737`.

| Run | Artifact(s) | Review result |
|---|---|---|
| `42870664509` | `13789830986` | 18 source-file governance implementation subset snapshot; not the 289-file exact-target snapshot |
| `42870617536` | `13790040735` | Batch artifact is stale for latest inventory: pins inventory SHA `88222e...` and ledger SHA `5aaa4a...` |
| `42870576974` | `13789592172` | 24 tests passed; 23 resume-identity mismatch cases rejected without checkpoint/manifest mutation; no pilot or cross-runner workflow dispatched in this run |
| `42870936071` | `13789382482` | Current inventory; target 1,800 records / 271 paths; main 711 records / 189 paths; both reconciliations pass |
| `42871210051` | `13788334234` | Exact target snapshot; 289/289 present, 292 extracted files checked, no errors, zero overlay records |
| `42870523334` | none | 31 V3 governance tests passed; new overwrite regression methods were not yet present in the test module |
| `42872743465` | none | Human overlay workflow failed at snapshot checksum verification; conversion/merge/upload did not run |
| `42870440350` | none | Engineering equivalence workflow failed at a test assertion-message mismatch; later equivalence tests skipped |
| `42870347767` | `13791811090` | Full-path engineering equivalence passed; six replicates, 1,000 surrogates each; not formal calibration |
| `42870298995` | `13789844889` | Assignment-matrix audit `PASS_ENGINEERING_ONLY`; A/B both cover indices 0–5; no mismatches |
| `42870239737` | `13790460003` worker 0; `13788219997` worker 1; `13789801310` worker 2; `13789491564` worker 3; `13788962393` worker 4; `13789032373` worker 5; `13789098160` connected reference; `13788489214` comparison | Six worker records exactly match their corresponding connected-reference records; six distinct runner instances; all same Linux platform; engineering only |
| `42870198624` | `13790215402` | 19 CLI resume identity fields tested; mismatches rejected; checkpoint and manifest unchanged |
| `42870135490` | `13789261860` | Two valid 200-surrogate diagnostic pilot attempts; p-values 0.1890547 and 0.0248756; not formal calibration |

## Artifact integrity hashes (downloaded ZIP bytes)

- `13789830986`: `ad9e725d48ccb3d7cfc23e6f3f7fa4c517ab771b6f8e71d721fb8e602731d56b`
- `13790040735`: `1086d489160a498e54087835c564cb9f63ca616f65417f6424ebd9932b6c445b`
- `13789592172`: `82750b7c81d4f2973fb10b9ccce600da85996d7014062fc1deb175f7db56fcdc`
- `13789382482`: `e844dd80fb1a082940838f35b2d82f2e3f479bfd46116dda662681fb26b731b1`
- `13788334234`: `8dd52ff8bd768244f3b12383f203d7bec0fd55b0b19e90d64adcab6cf2c53baa`
- `13791811090`: `3c53c06b75a4c7b35176faddd30901b035770658179e071ccccd613e5c1ac145`
- `13789844889`: `f190613b94030f201d79f89c6efcb1a977bc1c30f0e1c5b182cf52e37d0a2bee`
- `13788489214`: `a7518e869a8ad90a8ceef6cbcabdc33eaa68d74cc4cf260b920a6eabc53a3ec1`
- `13790215402`: `8d0f24e9d3cffb714bf7e30987b25844e2fa80950e2a53cff0c8fd5b1ea354fa`
- `13789261860`: `a2044c3109c15b2c28aafc2f4a3eca147d93b2188ca6770f20f23b396b2d24af`
- `13790460003`: downloaded and inspected; worker 0 artifact, one valid record, no missing/invalid attempts
- `13789801310`: downloaded and inspected; worker 2 artifact, one valid record, no missing/invalid attempts
- `13789491564`: downloaded and inspected; worker 3 artifact, one valid record, no missing/invalid attempts
- `13789098160`: downloaded and inspected; connected reference artifact, six valid records
- `13789032373`: downloaded and inspected; worker 5 artifact, one valid record, no missing/invalid attempts
- `13788962393`: downloaded and inspected; worker 4 artifact, one valid record, no missing/invalid attempts
- `13788219997`: downloaded and inspected; worker 1 artifact, one valid record, no missing/invalid attempts

The seven worker/reference artifact SHA-256 values are not repeated here because the decisive identity checks are the embedded payload manifests and the exact record comparisons against the comparison artifact. The package manifest records hashes for package files, not these external artifacts.
