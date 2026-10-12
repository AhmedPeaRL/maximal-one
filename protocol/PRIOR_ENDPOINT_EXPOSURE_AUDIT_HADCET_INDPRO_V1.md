# Prior Endpoint Exposure Audit — HadCET and INDPRO — V1

**Status:** Researcher statement recorded; historical run/artifact audit pending. This is not a preregistration and does not claim that no endpoint values were ever computed.

## Researcher statement

On 2026-10-12, the researcher stated: “We did not view the endpoint results for HadCET and INDPRO before completing the preanalysis protocol.” Preserve this statement as the researcher's report of personal exposure.

## Separate questions that must not be conflated

- **Computed:** Did a workflow, script, notebook, or artifact generate endpoint alpha, p-values, endpoint plots, or outcome summaries before the decision commit?
- **Displayed:** Did any log, artifact preview, report, conversation, or notification display those values?
- **Viewed:** Did the researcher actually inspect the endpoint values or plots before the decision?
- **Decision timing:** Was the final technical choice committed before the endpoint was computed or viewed?

The researcher statement answers the personal-viewing question as reported. It does not, by itself, answer whether a prior workflow computed or exposed results in a log/artifact, nor does it establish a timestamped preregistration.

## Audit table — complete from source records

| Record | Exact run/commit/artifact | Endpoint values generated? | Endpoint values displayed? | Researcher viewed before decision? | Evidence / notes |
|---|---|---|---|---|---|
| GitHub Actions history for HadCET | `TO_BE_REVIEWED` | `UNKNOWN` | `UNKNOWN` | `NO, per researcher statement; verify records` | `TO_BE_COMPLETED` |
| GitHub Actions history for INDPRO | `TO_BE_REVIEWED` | `UNKNOWN` | `UNKNOWN` | `NO, per researcher statement; verify records` | `TO_BE_COMPLETED` |
| Prior chat/report records | `TO_BE_REVIEWED` | `UNKNOWN` | `UNKNOWN` | `NO, per researcher statement; verify records` | `TO_BE_COMPLETED` |
| Preanalysis decision commit | `TO_BE_COMPLETED` | n/a | n/a | n/a | `TO_BE_COMPLETED` |

## Audit procedure

1. Search Actions history for workflows that load HadCET or INDPRO, run `estimate_alpha`, compute a p-value, generate endpoint plots, or write endpoint-specific artifacts.
2. For each relevant run, record the run ID, workflow name, commit SHA, timestamp, artifact name/ID, and whether the endpoint value itself is present in logs or files. Download the artifact when possible; do not infer contents from the artifact name alone.
3. Search the project's prior reports/conversations for endpoint-specific numeric values or plots before the final protocol commit.
4. Record the researcher's statement separately from machine evidence. Do not upgrade `UNKNOWN` to `NO` merely because a search did not find a value.
5. Complete and commit the technical preanalysis choices before any fresh endpoint calculation or inspection.

## Classification rule

- If an endpoint was computed or viewed before the technical decision, classify that analysis as exploratory/post-observation; any future confirmatory analysis must be prospective and based on a committed protocol.
- If the evidence remains incomplete, preserve `UNKNOWN` for the unresolved machine/display question and retain the researcher's statement as reported.
- Only if timestamped evidence establishes that the relevant decision was committed before computation and exposure may the prospective status be described narrowly for that decision. Do not retroactively label older results preregistered.

## Current scientific status

HadCET and INDPRO remain `NOT APPROVED FOR REPLICATION`. No endpoint analysis is authorized by this audit file. `claim_promotion_authority = false`.
