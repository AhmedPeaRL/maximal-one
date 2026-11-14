# P0 Remediation Patch Guide — Review Branch Only

**Target source reviewed:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`  
**Do not apply to `main`.** These are proposed changes for `review/type1-v4-remediation` only. They require local tests and independent review before any merge decision.

This guide addresses the highest-impact trust boundaries identified in the exact snapshot. It does not close any scanner finding by itself.

---

## 1. `scientific-validation.yml`: remove untrusted payload from shell source

### 1.1 Replace the `Stage witness as run-local artifact` step

The `65536`-byte check below is a proposed defensive cap, not a limit established by the current protocol. Confirm the documented maximum `repository_dispatch` payload size and the project contract before accepting it; if the intended payload may be larger, set a justified bound and add a boundary test.

The current step inserts `toJson(github.event.client_payload)` directly into a single-quoted shell assignment. Replace the complete step with:

```yaml
      - name: Stage witness as run-local artifact
        shell: bash
        env:
          CLIENT_PAYLOAD_JSON: ${{ toJson(github.event.client_payload) }}
        run: |
          set -euo pipefail
          python - <<'PY'
          import json
          import os
          from pathlib import Path

          raw = os.environ.get("CLIENT_PAYLOAD_JSON", "null")
          if len(raw.encode("utf-8")) > 65536:
              raise SystemExit("client payload exceeds 64 KiB")

          if raw in ("", "null"):
              payload = {"_empty": True}
          else:
              payload = json.loads(raw)

          if not isinstance(payload, dict):
              raise SystemExit("client payload must be a JSON object")

          out = Path("artifacts/witness_ingestion/payload.json")
          out.parent.mkdir(parents=True, exist_ok=True)
          out.write_text(
              json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
              encoding="utf-8",
          )
          PY
          sha256sum \
            artifacts/witness_ingestion/payload.json \
            > artifacts/witness_ingestion/payload.sha256
          echo "Witness staged locally only."
          echo "No witness file will be written to data/external/."
```

### 1.2 Change only the payload-construction preamble in `Validate witness payload`

Do **not** replace or shorten the complete step. Keep the existing step name and the complete Node validation program verbatim. Add the following step-level `env` block and replace only the current shell lines that assign `RAW` and write `payload.json` (the current lines 1529–1536) with the Python block below. Leave the existing `node - <<'NODE'` block and all of its validation logic untouched.

```yaml
      - name: Validate witness payload
        env:
          CLIENT_PAYLOAD_JSON: ${{ toJson(github.event.client_payload) }}
        run: |
          set -euo pipefail
          python - <<'PY'
          import json
          import os
          from pathlib import Path

          raw = os.environ.get("CLIENT_PAYLOAD_JSON", "null")
          if len(raw.encode("utf-8")) > 65536:
              raise SystemExit("client payload exceeds 64 KiB")
          payload = {"_empty": True} if raw in ("", "null") else json.loads(raw)
          if not isinstance(payload, dict):
              raise SystemExit("client payload must be a JSON object")
          Path("payload.json").write_text(
              json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
              encoding="utf-8",
          )
          PY
          # Keep the existing `node - <<'NODE'` block here, unchanged.
```

The last comment is an instruction to retain the existing Node block; it is not a literal replacement for that block.

### 1.3 Replace the `Log Input` and `Generate Hash` steps

Both steps currently interpolate `github.event.client_payload.input` directly into `run:`. Replace them with one step so the input is parsed as data, never as shell code:

```yaml
    - name: Log and hash external input safely
      shell: bash
      env:
        CLIENT_PAYLOAD_JSON: ${{ toJson(github.event.client_payload) }}
      run: |
        set -euo pipefail
        python - <<'PY'
        import hashlib
        import json
        import os
        from pathlib import Path

        raw = os.environ.get("CLIENT_PAYLOAD_JSON", "null")
        if len(raw.encode("utf-8")) > 65536:
            raise SystemExit("client payload exceeds 64 KiB")
        payload = {} if raw in ("", "null") else json.loads(raw)
        if not isinstance(payload, dict):
            raise SystemExit("client payload must be a JSON object")
        value = payload.get("input", "")
        if not isinstance(value, str):
            raise SystemExit("client_payload.input must be a string")

        Path("data").mkdir(parents=True, exist_ok=True)
        with Path("data/external_log.txt").open("a", encoding="utf-8") as f:
            f.write("INPUT: " + value + "\n")

        # Match the prior `echo ... | sha256sum` newline behavior.
        digest = hashlib.sha256((value + "\n").encode("utf-8")).hexdigest()
        with Path("data/hash_log.txt").open("a", encoding="utf-8") as f:
            f.write(digest + "  -\n")
        PY
```

### 1.4 Required negative tests before calling this mitigated

Run test payloads containing, at minimum:

- `' ; touch /tmp/HCM_INJECTION_MARKER ; #`
- `"$(touch /tmp/HCM_INJECTION_MARKER)"`
- backticks, semicolons, `&&`, pipes, dollar signs, and embedded newlines;
- Unicode and long strings near the accepted size limit;
- missing, null, array, number, and object values for `input`.

Acceptance requires: no marker command executes; JSON round-trip is correct; the stored input bytes and SHA-256 are correct; invalid types and oversized payloads fail closed. Also add a static regression test that rejects `${{ github.event.client_payload... }}` or `${{ toJson(github.event.client_payload) }}` inside any `run:` block in this workflow.

---

## 2. `scientific-validation.yml`: least-privilege permissions and secret scope

### 2.1 Replace workflow-level permissions

Replace the current broad workflow-level permission block with this read-only baseline:

```yaml
permissions:
  contents: read
```

Then add this job-level block to `core-proof` only, because that job runs CodeQL init/analyze in the scanned workflow:

```yaml
  core-proof:
    permissions:
      contents: read
      actions: read
      security-events: write
```

The existing `verify-core` and `claim-gate` jobs already declare read-only job permissions. Keep those. Other jobs should inherit only `contents: read` unless a line-by-line audit proves an additional permission is necessary. Do not restore `packages: write`, `pages: write`, or `id-token: write` merely because they were previously present at workflow level.

**Caution:** `core-proof` also pushes to `main` using the custom `GH_TOKEN` secret in the current source. That is not a reason to grant `contents: write` to the workflow's built-in `GITHUB_TOKEN`. Keep the custom token scoped to the exact job that needs it and separately verify that its credential is a repository-scoped fine-grained token (or an appropriately restricted GitHub App token) with only the required repository Contents write permission.

### 2.2 Move secrets out of workflow-level `env`

Remove these secret-backed values from the workflow-level `env` block:

```yaml
  GH_TOKEN: ${{ secrets.GH_TOKEN }}
  WITNESS_SECRET: ${{ secrets.WITNESS_SECRET }}
  GH_REPO: ${{ secrets.GH_REPO }}
  EXTERNAL_SOURCE_URL: ${{ secrets.EXTERNAL_SOURCE_URL }}
```

Then scope them only where used:

- `core-proof`: `GH_TOKEN` and `GH_REPO` (the current push-to-main script around line 1385).
- `external-collision`: keep its existing job-level `GH_TOKEN` and `GH_REPO` declarations.
- `build-report`: keep its existing job/step-level `GH_TOKEN` declaration.
- `sweep-plus`: keep `GH_TOKEN` only in the steps/jobs that use it (current references around lines 4827 and 4957).
- `ingest-witness`: keep `WITNESS_SECRET` only in the exact step that consumes it (current reference around line 1611).
- `EXTERNAL_SOURCE_URL`: the exact scanned workflow contains no further reference after its workflow-level declaration. Confirm no indirect use is intended, then remove the unused declaration.

Also replace direct secret interpolation in the mask step with step-level `env` values, for example:

```yaml
      - name: Mask scoped credentials
        env:
          GH_TOKEN_TO_MASK: ${{ secrets.GH_TOKEN }}
          WITNESS_SECRET_TO_MASK: ${{ secrets.WITNESS_SECRET }}
        run: |
          echo "::add-mask::$GH_TOKEN_TO_MASK"
          echo "::add-mask::$WITNESS_SECRET_TO_MASK"
```

Only include a secret in this step if that step actually needs to mask it; do not broaden secret scope just to mask a value that is not otherwise available to the job.

---

## 3. Full candidate replacement: `.github/workflows/build-image.yml`

The current workflow publishes `ghcr.io/<repo>:latest` for every push and also declares `packages: write` for `pull_request`. Run `43614085900` confirms that a push to `review/type1-v4-remediation` at commit `283d1b7a1800fdc7a1e63dbd33878827a1b3759e` reached the `Push image` step successfully. Replace the workflow with the candidate below so all branches/PRs can build and test, but only a trusted push to `main` can publish.

The action references below are pinned to commit SHAs resolved from the official upstream tag refs during this review:

- `actions/checkout` v6: `d23441a48e516b6c34aea4fa41551a30e30af803`
- `actions/setup-python` v6: `ece7cb06caefa5fff74198d8649806c4678c61a1`

```yaml
name: Build and Publish Container

on:
  push:
  pull_request:
    branches: [main]

permissions: {}

jobs:
  build:
    name: Build without registry credentials
    runs-on: ubuntu-24.04
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6
        with:
          python-version: "3.11.8"

      - name: Install hash-checked dependencies
        run: |
          python -m pip install --upgrade pip==24.0
          python -m pip install --require-hashes -r requirements-lock.txt

      - name: Build image without pushing
        env:
          IMAGE_NAME_RAW: ghcr.io/${{ github.repository }}
        run: |
          set -euo pipefail
          IMAGE_NAME="$(printf '%s' "$IMAGE_NAME_RAW" | tr '[:upper:]' '[:lower:]')"
          docker build -t "${IMAGE_NAME}:ci-${GITHUB_SHA}" .

  stability-check:
    name: Scientific stability checks
    runs-on: ubuntu-24.04
    container:
      image: python:3.11.8-slim
    needs: build
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          persist-credentials: false

      - name: Install hash-checked dependencies
        run: |
          python -m pip install --upgrade pip==24.0
          python -m pip install --require-hashes -r requirements-lock.txt

      - name: Run SDP robustness test
        run: python stability/sos_robustness_test.py

      - name: Spectral gap check
        run: python stability/spectral_gap_test.py

      - name: Eigenvalue drift
        run: python stability/eigen_drift_check.py

  publish:
    name: Publish trusted main-branch image
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    needs: [build, stability-check]
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          persist-credentials: false

      - name: Log in to GHCR
        env:
          REGISTRY_USER: ${{ github.actor }}
          REGISTRY_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          set -euo pipefail
          printf '%s' "$REGISTRY_TOKEN" | docker login ghcr.io \
            --username "$REGISTRY_USER" --password-stdin

      - name: Build and publish immutable SHA tag and latest
        env:
          IMAGE_NAME_RAW: ghcr.io/${{ github.repository }}
        run: |
          set -euo pipefail
          IMAGE_NAME="$(printf '%s' "$IMAGE_NAME_RAW" | tr '[:upper:]' '[:lower:]')"
          docker build -t "${IMAGE_NAME}:${GITHUB_SHA}" -t "${IMAGE_NAME}:latest" .
          docker push "${IMAGE_NAME}:${GITHUB_SHA}"
          docker push "${IMAGE_NAME}:latest"
```

**Compatibility gate before accepting this replacement:** the current `requirements-lock.txt` pins SciPy `1.11.4`, while the old `build-image.yml` installed SciPy `1.12.0`. This candidate deliberately aligns the build and stability jobs to the repository lock file. Run the workflow and verify all three stability scripts and the Docker build before treating the change as accepted. If SciPy `1.12.0` is required, update the canonical input/lock files prospectively with hashes and tests; do not keep an untracked ad-hoc dependency set in this workflow.

The `publish` job is intentionally restricted to `push` on `main`. If the project later adopts a release-tag process, replace this condition with an explicit, reviewed release-tag policy; do not allow review-branch or pull-request events to publish `latest`.

---

## 4. `release-lock.yml`: downstream workflow-run trust boundary

The scanner identifies `workflow_run` at the trigger and an automatic Node package-manager cache path. The workflow also grants `contents: write`, pushes tags, and creates releases. Apply these changes only after identifying the exact upstream workflow named `Deterministic Scientific Mesh`.

1. Neither the exact target snapshot nor either uploaded full-repository ZIP (main at `160acfc...`, review at `c44b5eb...`) contains a workflow named `Deterministic Scientific Mesh`. The `release-lock.yml` trigger is therefore orphaned/inactive in the inspected source states, unless another workflow source exists outside those snapshots. Do not mark it mitigated: remove the dormant workflow or identify and bind it to the intended upstream workflow with an explicit workflow-ID/branch/event guard before enabling it.
2. After confirming the expected upstream workflow ID, constrain the downstream job to a successful trusted push on the repository's `main` branch. A starting guard is:

```yaml
    if: >-
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.event == 'push' &&
      github.event.workflow_run.head_branch == 'main' &&
      github.event.workflow_run.head_repository.full_name == github.repository
```

Add an explicit check for the expected `workflow_id` once it has been verified from GitHub; do not invent that ID.

3. Pin the existing actions to verified SHAs. Candidate tag resolutions obtained from the official upstream tag refs during this review:
   - `actions/setup-node` v4: `49933ea5288caeca8642d1e84afbd3f7d6820020`
   - `softprops/action-gh-release` v2: `3bb12739c298aeb8a4eeaf626c5b8d85266b0e65`
4. Disable automatic package-manager caching for the privileged workflow:

```yaml
      - name: Setup Node
        uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4
        with:
          node-version: 18.20.8
          package-manager-cache: false
```

5. The exact target commit contains a root `package.json` and `package-lock.json` (lockfileVersion 3); `package.json` defines the `validate` script as `node ./core-scientific/publication-gate/generate-report.cjs`. The lock currently contains only the root package and no dependencies. Prefer `npm ci` over `npm install` for lockfile enforcement, then run `npm run validate` and verify the generated report before any tag/release operation.

`evolution.yml` also uses `workflow_run`, but in the exact snapshot it only runs an `echo` after `Evaluation Gate` and has no explicit write permission or artifact consumption. Its scanner warning should be reviewed contextually; do not assign it the same impact as `release-lock.yml` without evidence.

---

## 5. Required verification after proposed changes

1. Run actionlint and zizmor against the exact new review-branch commit.
2. Confirm the four `scientific-validation.yml` payload expressions no longer occur inside `run:` source.
3. Run adversarial payload tests and prove no command execution.
4. Inspect the effective permissions for every job; prove no untrusted event can reach a write-capable job.
5. Push a harmless documentation-only commit to the review branch and verify `build` and `stability-check` run while `publish` is skipped.
6. Open a test PR and verify no registry login or push step runs.
7. Push to `main` only after independent approval and verify the publish job has only `packages: write` and emits both the SHA tag and `latest`.
8. Verify the registry digest and record it; do not infer the digest from a successful step alone.
9. For `release-lock`, test PR-originated workflow runs, non-main branches, wrong upstream workflow IDs, and failed runs; all must be blocked before any tag/release operation.
10. Record each fix against the exact finding IDs in the CSV registers, then rerun the scanners on that exact commit.

No item in this guide authorizes a merge, protocol freeze, formal calibration, confirmatory execution, claim support, or promotion.
