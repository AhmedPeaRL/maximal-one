# HCM External Reproduction — Scope and Acceptance Specification V1

**Target branch:** `review/type1-v4-remediation`  
**Observed baseline:** `45b647ce2a6d2cbea1fe08e874be60b738f472c1`  
**Main:** frozen  
**Public service/deployment:** not authorized

## 1. Critical terminology

The project must distinguish three different claims:

1. **Artifact retrieval/integrity:** downloading an existing report and hashing it. This proves only that bytes were retrieved and hashed.
2. **Clean-checkout computational reproducibility:** checking out an exact source commit in a fresh working directory/environment, rerunning the same project's implementation against identified inputs, and comparing outputs. This is valuable, but it uses the same implementation and is not an independent implementation.
3. **Independent scientific replication:** an independent researcher/team, with independent analytical execution and documented data/protocol provenance, tests the scientific claim. A self-invoked script cannot establish this by itself.

No output may promote claim 1 into claim 2 or claim 2 into claim 3.

## 2. Current defects

### `api/public_reproduce_endpoint.py`
The old function is not an HTTP route. It cloned the repository's mutable default branch, installed dependencies during a request, had no process timeout or resource isolation, wrote a payload that the called script did not read, and expected `artifacts/reproduction_result.json`, which the called script did not create.

### `analysis/external_reproduction.py`
The old script fetched a fixed GitHub Pages JSON file, checked two fixed numeric fields, and printed pass/fail. It did not run the analysis, consume a caller payload, establish a clean environment, or create a reproducibility result. It is not independent reproduction.

Both legacy helpers should fail closed until replaced by a reviewed design. The replacement stubs in this kit intentionally perform no network, subprocess, or scientific work.

## 3. Existing clean-checkout runner

`analysis/true_independent_reproduction.py` is the correct starting point for a *clean-checkout computational reproducibility* tool, not an independent scientific replication tool. It:
- requires `GITHUB_SHA`;
- checks out that commit in a fresh clone;
- rebuilds canonical inputs;
- runs `scripts/generate_report.py --seed 42 --canonical`;
- compares normalized report structure and fingerprint;
- records that independent implementation, laboratory, and scientific replication are false.

Before relying on it, harden and test:
- validate the commit as exactly 40 lowercase hexadecimal characters;
- fetch the exact commit explicitly and verify `git rev-parse HEAD`;
- apply a timeout to every network/process command;
- install from the lockfile with `--require-hashes` in a disposable environment;
- scrub GitHub tokens and other credentials from the child environment;
- set deterministic thread/environment controls;
- bind the local baseline report, data manifest, input hashes, source commit, Python version, dependency lock hash, and output hash in one manifest;
- fail closed if required source data or canonical report is absent;
- never silently normalize away scientific output fields; every excluded volatile field must be predeclared and justified;
- retain the full raw output and normalized comparison output;
- emit a nonzero exit status on any mismatch or incomplete evidence;
- set all scientific promotion/replication authority fields to false.

## 4. Required runner contract

A future runner must accept explicit immutable inputs:
- repository identity;
- exact 40-character source commit;
- canonical input/data manifest and hashes;
- dependency lockfile hash;
- fixed seed and declared numerical/thread settings;
- output directory.

It must not accept arbitrary shell commands, arbitrary repository URLs, arbitrary package indexes, or unbounded input payloads.

It must:
1. validate all arguments before starting subprocesses;
2. verify the target commit is reachable from the approved Review repository and check out that exact SHA;
3. verify the data manifest and every input hash before computation;
4. create a disposable environment from the hash-locked dependency file;
5. run with a strict wall-clock timeout and bounded CPU/memory/disk;
6. avoid privileged credentials and avoid persisting Git credentials;
7. record stdout/stderr and every command's exit status;
8. preserve raw outputs and generate a deterministic manifest;
9. compare only preregistered scientific fields and separately report exact-hash agreement;
10. fail closed on missing inputs, unexpected output schema, timeout, nonzero exit, or mismatch.

A local subprocess timeout is not a complete sandbox. Strong isolation requires a container/VM or dedicated runner with resource limits and a restricted network policy. Do not expose this as a public multi-tenant service without a separate threat model and security review.

## 5. Acceptance tests

- missing commit rejected;
- malformed SHA rejected;
- a different commit checked out rejected;
- missing canonical dataset rejected;
- altered input hash rejected;
- dependency lock mismatch rejected;
- payload with shell metacharacters treated as data, never evaluated;
- subprocess timeout terminates the run and records failure;
- nonzero pipeline exit produces failure;
- missing report or invalid JSON produces failure;
- changed scientific field produces mismatch;
- unapproved normalization field is rejected;
- no token/secret appears in child environment or artifacts;
- report includes exact commit, input hashes, lock hash, runtime versions, output hash, and command exit statuses;
- all scientific replication/promotion authority fields remain false.

## 6. What this can and cannot prove

A passing clean-checkout replay supports computational reproducibility of the specified code/data/environment combination. It does not prove:
- that the estimator or statistical model is scientifically appropriate;
- that the dataset is representative or independent;
- that the result is robust to alternative reasonable analytical choices;
- that an independent implementation agrees;
- that a separate laboratory/team replicated the result;
- that any scientific claim is confirmed.

Independent scientific replication remains dependent on the human reviewers and genuinely independent work.
