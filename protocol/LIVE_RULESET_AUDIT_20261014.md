# Live GitHub Ruleset Audit — 2026-10-14

Status: `LIVE_CONFIGURATION_READ; TARGETING_REQUIRES_OWNER_DECISION`

Repository: `AhmedPeaRL/maximal-one`

Ruleset: `Evolution Gate`

Ruleset ID: `12957369`

Live settings URL: https://github.com/AhmedPeaRL/maximal-one/rules/12957369

Read-only API resource: https://api.github.com/repos/AhmedPeaRL/maximal-one/rulesets/12957369

## Observed live targeting

- Enforcement: `active`
- Target: `branch`
- Include: `~DEFAULT_BRANCH`
- Exclude: `refs/heads/main`

The workflow and repository context identify `main` as the default branch. If `~DEFAULT_BRANCH` resolves to `main`, the include/exclude combination leaves this ruleset with no effective target branch. Therefore, do not assume this ruleset protects `main`.

## Live rules differ from the repository JSON snapshot

The live ruleset currently reports, among other settings:

- Pull request approval count: `10`
- Required status checks include `Evolution Gate` (listed twice, once with integration ID `15368`)
- Required linear history
- Code scanning and code quality requirements
- Copilot code review
- Required deployment environments
- Required signatures
- Branch creation rule

The committed `.github/rulesets/evolution-gate.json` instead records approval count `0` and does not contain all the live rule types. It is a repository file, not an automatic source of truth for the live GitHub ruleset.

## Safe decision

Do not edit the committed JSON and assume the live setting changed. Do not change the live ruleset blindly: an overly strict or mis-targeted ruleset can block the repository owner from merging changes. First decide which branches should be protected and whether the approval/deployment requirements are feasible for this solo-maintained repository. Then adjust the actual ruleset in GitHub Settings and separately update the committed snapshot to match the verified live state.

This audit is configuration evidence only; it is not scientific evidence and does not affect the null protocol or claim status.
