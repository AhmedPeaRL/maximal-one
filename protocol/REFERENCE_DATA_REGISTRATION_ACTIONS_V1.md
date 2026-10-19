# Empirical Reference-Data Registration — Required Actions

**Current state:** `TEMPLATE_NOT_REGISTERED`  
**Freeze state:** `NOT_FROZEN`  
**Claim support / promotion authority:** `false`

The existing `protocol/REFERENCE_DATA_REGISTRATION_TEMPLATE_V1.json` is a blank template, not evidence that data have been registered or independently approved. Do not invent hashes, source vintages, timestamps, reviewer names, or approval dates.

For each empirical series intended for later use:
1. Record publisher, stable URL/citation, variable/domain, and source vintage.
2. Preserve the original raw file byte-for-byte; never overwrite an earlier snapshot.
3. Record retrieval time in UTC and compute SHA-256 on the raw bytes before parsing.
4. Record a separate SHA-256 for the parsed representation, parser/version, cadence/window, expected observation count, missingness policy, and preprocessing.
5. Record prior exposure as `YES`, `NO`, or `UNKNOWN`; never convert `UNKNOWN` to `NO`.
6. Register the exact snapshot path and hashes before endpoint computation or calibration use.
7. Obtain an identifiable independent review of provenance, hashes, source revisions, cadence/gaps, missingness, shared nuisance drivers, exposure, and replication independence.
8. Record the reviewer's identity, expertise, conflicts, date, decision, and rationale. Do not use the assistant as a substitute for external independent sign-off.
9. A changed source file requires a new immutable entry and hash.
10. Empirical series are not known-truth Type-I data and do not automatically count as independent replication domains.

The latest raw-acquisition audit is blocked by structural/missingness issues. Do not compute the endpoint on blocked candidates until the audit is corrected and rerun under a committed protocol.
