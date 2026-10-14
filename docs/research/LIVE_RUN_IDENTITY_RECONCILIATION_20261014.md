# Live Run Identity Reconciliation — 2026-10-14

## Purpose

Record the verified identity of the latest inspected GitHub Actions run without conflating it with previously inspected archives or earlier workflow runs.

---

## Verified live run

- Repository: "AhmedPeaRL/maximal-one"
- Branch: "main"
- Workflow run ID: "38514166999"
- Workflow commit SHA: "ede924eba87f655eab7deb1b03a0d90274b24ba9"
- Commit message: "Fix artifact upload path and ensure newline at end"
- Commit URL: https://github.com/AhmedPeaRL/maximal-one/commit/ede924eba87f655eab7deb1b03a0d90274b24ba9
- Workflow URL: https://github.com/AhmedPeaRL/maximal-one/actions/runs/38514166999

---

## Identity evidence

The "core-proof" logs show the same full commit SHA for the checked-out repository revision, the verified workflow commit, and "GITHUB_SHA".

The workflow artifacts inspected for run "38514166999" report the same "head_sha".

This establishes the identity of the inspected live run and its associated artifacts.
It does not establish scientific claim support or independent scientific replication.

---

## Observed workflow outcome

- Core proof job: success.
- Build-report job: success.
- Node compute jobs: success.
- Final replication-eligibility gate: failure.
- Eligible independent replication domains: "0/2".
- Scientific claim status: "under_investigation".
- Scientific claim promotion: not established.

The gate failure is consistent with the declared requirement for two eligible independent replication domains.

---

## Public artifact availability

The workflow logs report HTTP 404 responses for public canonical-report retrieval paths. The public artifact consistency audit must therefore remain "UNAVAILABLE" when retrieval cannot be completed.

A fingerprint match is not equivalent to independent scientific reproduction.

---

## Archive identity remains separate

Previously inspected ZIP archives with different SHA-256 values must not be attributed to this run unless their contents and identity are independently matched to this exact commit.

The archive SHA-256 "2ca1cec1..." and the previously reported archive SHA-256 "b566e591..." are not interchangeable identities. Their relationship to the live commit remains unresolved until verified.

---

## Required follow-up

1. Remove the two literal-star files using exact-path deletion.
2. Normalize the repository-owner casing in the public URL constants.
3. Resolve the canonical-report publication path and verify that it returns the intended JSON rather than a 404 page.
4. Preserve "0/2" replication eligibility until two domains satisfy the declared criteria.
5. Do not change scientific thresholds, claim status, or promotion authority to force a passing result.
6. Record the next run ID, "GITHUB_SHA", checked-out "git rev-parse HEAD", and artifact IDs together.

---

## Interpretation boundary

This document is an identity and workflow audit record. It is not evidence that HCM's scientific claim has been established, that independent real-domain replication exists, or that the model's proposed consciousness mechanism has been demonstrated.
