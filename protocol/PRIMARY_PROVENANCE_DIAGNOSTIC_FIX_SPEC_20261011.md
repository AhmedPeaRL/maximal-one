# Diagnostic Fix Specification — Primary and Non-Replication Dataset Reasons

## Problem observed

The supplied `scientific-claim-promotion.yml` log prints the primary `sunspots` row with both:

- `reason: eligible`
- `reason: primary_domain_excluded_from_secondary_replication_count`
- `reason: missing_provenance_registry_entry`

The first message describes a structural check, not final replication eligibility. The last message is not a meaningful exclusion reason for the primary dataset because the primary is explicitly excluded from the secondary replication count by design. Derived controls and null controls similarly do not need provenance approval to establish that they are ineligible to count as independent replication.

This is a **diagnostic clarity defect**, not a reason to change the eligibility outcome. The current count `0/2` remains correct under the supplied policy.

## Intended behavior of a future code-only diagnostic patch

1. Preserve all existing eligibility booleans and all gate exit conditions.
2. Report structural measurement/length outcome separately from final replication outcome, e.g. `structural_status=MEASUREMENT_VALID` and `final_replication_eligible=false`.
3. For the primary domain, report `primary_domain_excluded_from_secondary_replication_count` as the applicable exclusion and do not add `missing_provenance_registry_entry` as though provenance could make the primary count as a secondary domain.
4. For derived, shuffled, synthetic, and null controls, report their role-based exclusion and do not clutter the final replication reason list with provenance missingness that cannot change their role-based ineligibility.
5. For independent secondary real domains, continue to report every applicable reason: structural threshold, provenance completeness/approval, timestamp/cadence integrity, independence, and null-adequacy status.
6. Add unit tests proving that these changes affect explanatory labels only. The same datasets must remain ineligible and the gate must still exit nonzero at `0/2`.

## Acceptance criteria

- No changes to `strict_claim.json`, `p <= 0.05`, the 1024 replication minimum, `nperseg=1024`, the null family, endpoint, tail, or acceptance thresholds.
- A test asserts the primary domain cannot be counted as secondary replication.
- A test asserts derived/null controls cannot be counted as independent real domains.
- A test asserts a structurally eligible but unapproved secondary domain remains `replication_eligible=false`.
- CI remains blocked while eligible independent secondary domains are fewer than two.

## Suggested commit message

`Clarify dataset eligibility diagnostics without changing gates`

This file is a specification, not an applied code change. Do not claim the diagnostic fix is implemented until code and tests are committed and a fresh run confirms the output.
