# HCM GitHub Actions remediation handoff — 2026-11-14

## Scope and verified snapshot

Repository: `AhmedPeaRL/maximal-one`

New review-branch commit supplied by the owner:
`1229ce760055de83fc07f77c050a59ce0a26eeb5`

The branch is still divergent from `main`: 467 commits ahead, 34 behind.
At the comparison time, `main` was `160acfc8600b66c7300f2fd0caa500972de740b8`.
Do not merge, rebase, or force-update `main` as part of this remediation.

### Latest supplied run: 43619850482

- Build without registry credentials: SUCCESS.
- Scientific stability checks: FAILURE during `contourpy==1.0.1` build because the `python:3.11.8-slim` job container lacked a working C++ compiler toolchain.
- Publish trusted main-branch image: SKIPPED.
- No workflow artifacts were attached to this run.
- Build job produced only a local image tag:
  `ghcr.io/ahmedpearl/maximal-one:ci-1229ce760055de83fc07f77c050a59ce0a26eeb5`
  This is not a registry push.

### Confirmed prior GHCR publication

Run `43614085900`, job `132505224850`, on review commit
`283d1b7a1800fdc7a1e63dbd33878827a1b3759e` successfully executed `docker push ...:latest`.

Registry output explicitly reported:

`sha256:5c930ed151cbba762d66ec2d0fc6e4de02637b6bc41455276e29069824899c96`

The prior workflow pushed the `latest` tag only. The exact historical registry version record, any later tag movement, and downstream consumers still require package/API inspection. Do not delete the package or digest.

## P0 — eliminate payload-to-shell injection

The current review-branch `scientific-validation.yml` still contains four shell interpolation sites:

- line 1510: `RAW='${{ toJson(github.event.client_payload) }}'`
- line 1529: same pattern
- line 3290: `echo "INPUT: ${{ github.event.client_payload.input }}" ...`
- line 3294: `echo "${{ github.event.client_payload.input }}" | sha256sum ...`

The two expression-only boolean conditions elsewhere are not shell source interpolation and are not the same sink. Keep them separately reviewed.

### Add these two files

Copy `analysis/safe_payload.py` and `tests/test_safe_payload_boundary.py` from this package into the repository.

Run locally/CI:

```bash
python -m unittest discover -s tests -p 'test_safe_payload_boundary.py' -v
```

### Replace the “Stage witness as run-local artifact” step

```yaml
      - name: Stage witness as run-local artifact
        env:
          CLIENT_PAYLOAD_JSON: ${{ toJSON(github.event.client_payload) }}
        run: |
          set -euo pipefail
          python analysis/safe_payload.py \
            --output artifacts/witness_ingestion/payload.json \
            --sha256 artifacts/witness_ingestion/payload.sha256
          echo "Witness staged locally only."
          echo "No witness file will be written to data/external/."
```

### Replace only the payload-construction preamble in “Validate witness payload”

Keep the existing complete Node validation block; do not replace it with a placeholder.

Replace:

```bash
RAW='${{ toJson(github.event.client_payload) }}'
if [ "$RAW" = "null" ] || [ -z "$RAW" ]; then
  echo '{"_empty": true}' > payload.json
else
  echo "$RAW" > payload.json
fi
```

with:

```bash
set -euo pipefail
test -s artifacts/witness_ingestion/payload.json
cp artifacts/witness_ingestion/payload.json payload.json
```

Then retain the current Node code that parses `payload.json`, rejects null, applies the existing size guard, and performs its other validation.

### Replace the two “Log Input” and “Generate Hash” steps

Use one step. It keeps the old hash convention of hashing the input plus the newline that `echo` previously added. The input is read as JSON data, not inserted into shell source.

```yaml
    - name: Log input and generate hash safely
      env:
        CLIENT_PAYLOAD_JSON: ${{ toJSON(github.event.client_payload) }}
      shell: bash
      run: |
        set -euo pipefail
        python - <<'PY'
        import hashlib
        import json
        import os
        from pathlib import Path

        raw = os.environ.get("CLIENT_PAYLOAD_JSON", "null")
        data = {"_empty": True} if raw in ("", "null") else json.loads(raw)

        value = data.get("input", "") if isinstance(data, dict) else ""
        if not isinstance(value, str):
            raise SystemExit("client_payload.input must be a string")

        Path("data").mkdir(parents=True, exist_ok=True)
        with Path("data/external_log.txt").open("a", encoding="utf-8") as f:
            f.write("INPUT: " + value + "\n")

        digest = hashlib.sha256((value + "\n").encode("utf-8")).hexdigest()
        with Path("data/hash_log.txt").open("a", encoding="utf-8") as f:
            f.write(digest + "  -\n")
        PY
```

Before accepting this logging change, inspect downstream consumers of `data/hash_log.txt`: the prior `sha256sum` output included a filename marker. If any consumer parses that exact format, preserve its required format explicitly and test it. Do not silently change a downstream data contract.

### Required negative-test acceptance

The tests in this package cover `$()`, backticks, semicolons, `&&`, `${IFS}`, quotes, and embedded newlines. They assert that hostile strings remain literal JSON data and that a marker command is not executed.

The workflow must run these tests before any job that handles external payloads. A green test alone is not enough: confirm by source inspection that no `github.event.client_payload.*` or `toJson(github.event.client_payload)` value is interpolated directly inside a `run:` script.

## P0 — fix stability job environment

The latest stability job failed before running its scientific checks. Its `python:3.11.8-slim` container could not compile `contourpy==1.0.1`; the Docker build job succeeded because its Docker build environment had the required compiler toolchain.

Preferred correction: install compiler tooling in the stability job before hash-locked dependency installation:

```yaml
      - name: Install system build tools
        shell: bash
        run: |
          set -euo pipefail
          apt-get update
          apt-get install -y --no-install-recommends build-essential
          rm -rf /var/lib/apt/lists/*
```

Place this immediately before `Install hash-checked dependencies` in `stability-check`.
Then rerun the workflow. This is a proposed environment fix, not a verified success. An alternative is to use a tested, pinned prebuilt dependency image or compatible wheel set; do not loosen hashes or silently change dependency versions.

## P1 — build/publish separation

The new `build-image.yml` is directionally correct:

- workflow-level permissions are `{}`.
- build and stability jobs only have `contents: read`.
- only the `publish` job has `packages: write`.
- publish requires a push to `refs/heads/main` and successful build + stability jobs.
- checkout credentials are not persisted.
- checkout and setup-python use full SHA pins.

Do not weaken the `publish` condition. Test that:
1. a push to `review/type1-v4-remediation` runs build/stability but skips publish;
2. a pull request to main skips publish;
3. a push to main publishes only after both required jobs succeed.

The latest run demonstrates case 1: publish was skipped. The stability job failure means the full success path has not yet been demonstrated.

## P1 — workflow-wide permissions and secrets

The current `scientific-validation.yml` still grants workflow-wide:

- `contents: write`
- `packages: write`
- `pages: write`
- `id-token: write`
- `security-events: write`

It also exposes these secrets as workflow-wide environment variables:
`GH_TOKEN`, `WITNESS_SECRET`, `GH_REPO`, `EXTERNAL_SOURCE_URL`.

Do not replace the permission block blindly until every job and every write operation has been inventoried. Required procedure:

1. Set the workflow default to the minimum read-only baseline only after confirming all jobs that write contents/pages/security events or request OIDC.
2. Add permissions at the individual job level only where a specific step requires them.
3. Move each secret from workflow-wide `env:` to the exact step/job that uses it.
4. Prefer `GITHUB_TOKEN` with a narrow permission over a long-lived PAT where supported.
5. Verify the token type, owner, scopes, expiration, and repository access of `GH_TOKEN`; never print the token.
6. Keep `WITNESS_SECRET` only in the signature-verification step. It must not be present in unrelated jobs.
7. Ensure untrusted PR/repository_dispatch paths cannot reach privileged jobs or secrets.

The exact per-job matrix remains OPEN until all jobs and their write paths have been checked. A successful scanner run is not a substitute for this review.

## P1 — release-lock / workflow_run

The current `release-lock.yml` remains unchanged and listens for:

`workflow_run: workflows: ["Deterministic Scientific Mesh"]`

That upstream workflow name was not found in the inspected main/review snapshots. Treat the release workflow as dormant/unresolved, not as safely guarded.

Immediate safe disposition: disable it by moving the file outside `.github/workflows/` (for example to `docs/disabled-workflows/release-lock.yml.txt`) until the intended upstream is identified.

Before re-enabling:
- record the upstream workflow file path and workflow ID;
- verify the upstream repository is exactly this repository;
- verify event is `push`, branch is `main`, conclusion is `success`;
- pin the exact `workflow_id` in the guard;
- use a least-privilege release job;
- use `npm ci`, not `npm install`, when the lockfile is valid;
- pin all actions by verified full SHA;
- test that pull requests, forks, other branches, and unrelated workflow runs cannot trigger release/tag creation.

Do not invent the workflow ID. Do not use a broad `workflow_run` success-only condition.

## P1 — action SHA pinning

The previous independent scanner artifact recorded 151 `unpinned-uses` findings. Do not bulk-replace `@vN` with guessed hashes.

For every action:
1. record `owner/repository`, declared version/tag, exact resolved commit SHA, upstream release/tag evidence URL, and date checked;
2. verify the SHA belongs to the intended upstream repository and release;
3. inspect the action source/change log and permissions;
4. pin to the 40-character SHA and leave a human-readable version comment;
5. run actionlint and zizmor against the exact candidate commit;
6. retain the before/after finding IDs and disposition.

A pin is not “verified” merely because it is a 40-character string.

## P1 — artipacked and remaining diagnostics

For every `artipacked` finding:
- inspect whether checkout credentials are persisted;
- use `persist-credentials: false` when git push/authentication is not required;
- if push is required, scope credentials to the exact step and remove them before artifacts/caches are created;
- never upload `.git/config`, `.git-credentials`, or a workspace containing live credentials;
- record file, line, job, data path, mitigation, test evidence, and reviewer approval.

For all other diagnostics, use one finding per register row with:
`OPEN`, `MITIGATED`, `ACCEPTED_WITH_RATIONALE`, `FALSE_POSITIVE_WITH_EVIDENCE`, or `NOT_APPLICABLE_WITH_EVIDENCE`.
No finding should be closed solely because the scanner workflow completed.

## P2 — scanner rerun and source binding

After changes are committed to the review branch:
- run actionlint, zizmor, and Scorecard against that exact commit;
- upload raw outputs, tool versions, source commit, workflow commit, and SHA-256 manifest;
- ensure the artifact manifest identifies the commit actually scanned;
- compare findings to the previous 205 zizmor / 97 actionlint baseline;
- do not claim a clean scan if online-only checks were skipped or a scanner exited nonzero.

## Independent review gate

The external human reviewer must be independent of the repository owner and AI-assisted remediation. The reviewer should receive:
- immutable commit SHA;
- source snapshot manifest and hashes;
- exact scanner outputs;
- finding registers and dispositions;
- tests and CI logs;
- explicit AI-assistance disclosure;
- a request to report expertise, conflicts, scope, limitations, and a signed/date-stamped decision.

No independent review has been received yet. Do not represent AI-assisted review as independent human review.
