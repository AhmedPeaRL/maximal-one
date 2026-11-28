# V9 Current Review Rebaseline — Required Before Workflow Edits

**Disposition:** REBASELINE_REQUIRED — DO NOT APPLY TARGET-SNAPSHOT LINE PATCHES TO CURRENT REVIEW HEAD.

- Repository: `AhmedPeaRL/maximal-one`
- V3 software assurance target scanned commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- V3 workflow-definition / review source commit: `87160e6469d323187916d375c11300158777d22b`
- Current Review branch HEAD checked read-only: `4ef3f359575b2e58df78a7154f1e53cf350674f4`
- Current Review tree: `7eef169398006a8757f8d196d205c8e997ce71d3`

A read-only tree comparison of all 35 unique paths represented in the Zizmor findings found **0 identical blobs, 33 changed blobs, and 2 paths absent from current Review**. Thus, none of the Zizmor path occurrences can be presumed to map to the same file bytes on current Review. The table below lists the six highest-priority workflow paths compared individually; the remaining 29 path comparisons are also DIFFERENT or ABSENT as recorded in the occurrence register and must be re-mapped before patching.

| Path | Target blob at scanned commit | Current Review blob | Result |
|---|---|---|---|
| `.github/workflows/scientific-validation.yml` | `64f101495831b575c47e96cc26303960f33e6bc8` | `99a1e14087e46345c8e4bffa7bb54ac20189348a` | DIFFERENT |
| `.github/workflows/null-type1-calibration.yml` | `4fec09473d8e4e5b6be3186287c60edf00a68a9a` | `659d3b74aa236b1b3cf94f7cf6313cb87f399fb5` | DIFFERENT |
| `.github/workflows/build-image.yml` | `f39251ba22f2c72705dd5973543996421f7ca8ea` | `f69d1d2ed375858210c55d743168537f1ba58a73` | DIFFERENT |
| `.github/workflows/cross-run-memory-verification.yml` | `437fde7542d44a9ddc31c70eaf6ff5360f6abe8b` | `9b9e939b0bb7c6cee9b4cda85da6487fe4a6f838` | DIFFERENT |
| `.github/workflows/scientific-claim-promotion.yml` | `6b10d6c2a032e6e46f5a1e7c5e7339e243afe4d3` | `b5f800670aec65e795ab0f5e485b1f944f1668b9` | DIFFERENT |
| `.github/workflows/release-lock.yml` | `bdd07c7553e1735ff79a9f2ae760a955df45e802` | ABSENT | ABSENT FROM REVIEW |

Additional path-level result: `.github/workflows/evolution.yml` and `.github/workflows/legacy/scientific-evaluation.yml` are absent from current Review.

## Mandatory handling

1. Treat the 205 Zizmor findings and 97 Actionlint diagnostic headers as evidence about the exact scanned target commit only. Do not assume they describe current Review HEAD without a fresh exact-commit scan.
2. Do not copy line-number-specific patches from the target snapshot into current Review. Re-read the complete current file and re-map every finding to its current path/line/AST location first.
3. Keep Main frozen. Do not restore the absent `release-lock.yml` to Review or edit Main as part of this handoff.
4. Do not run any workflow yet. A new scan should be planned only after a reviewed patch set exists and the user explicitly authorizes a run.
5. Keep all 205 findings OPEN until each occurrence has an evidence-backed disposition and independent human review. The 3 V9 human-adjudication rows remain OPEN/PENDING; no scientific authority is granted.

## Current disposition

`TARGET_SNAPSHOT_TRIAGE_REGISTERED; CURRENT_REVIEW_REBASELINE_REQUIRED; NO_WORKFLOW_PATCH_AUTHORIZED; NO_FINDINGS_CLOSED; NO_AUTHORITY; MAIN_FROZEN`
