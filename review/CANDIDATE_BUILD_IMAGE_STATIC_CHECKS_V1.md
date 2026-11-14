# Candidate build-image workflow — static check record

Candidate: `candidate-workflows/.github/workflows/build-image.yml`

The candidate was extracted from `TYPE1_P0_REMEDIATION_PATCH_GUIDE_V1.md` and checked locally using the exact tool binaries bundled in the downloaded Software Assurance V3 artifact:

- actionlint 1.7.12: exit 0; no diagnostics.
- zizmor 1.30.1: JSON output contained zero findings in offline mode. The CLI reported offline mode and three suppressed checks; online-only audits were not performed.

This is a syntax/static triage check of the candidate workflow only. It is not an execution test, not a container build, not a registry test, and not independent security approval. The candidate has not been committed or run on GitHub Actions.
