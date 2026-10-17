# Cosmic-Ray Time-Integrity Review — 2026-10-17

**Dataset:** `real-data/cosmic_rays.csv` → `real-data/cosmic_rays_clean.csv`  
**Status:** `BLOCKED_NOT_REPLICATION_ELIGIBLE`  
**Role:** data-integrity diagnostic only

## Reproduced audit result

The repository's timestamp-aware audit was run against the supplied snapshot. It returned exit code `1`, correctly blocking replication use.

- Raw timestamped observations: `3,698`
- First timestamp: `2021-11-04 22:00:00+00:00`
- Last timestamp: `2023-12-31 23:00:00+00:00`
- Timestamp values valid: `true`
- Timestamps strictly increasing: `true`
- Timestamps unique: `true`
- Expected cadence: exactly `3,600` seconds
- Non-hourly intervals: `321`
- Intervals longer than one hour: `321`
- Longest uninterrupted hourly run: `486`
- Raw/clean row count and value order match: `true`
- Required replication minimum: `1,024`
- Replication eligible: `false`
- Approved for replication: `false`

The clean file's values match the raw file in order, but the clean pipeline input contains values only and drops the timestamps. This is not a cosmetic metadata problem: the raw series itself fails the current exact-hourly continuity requirement, and the longest contiguous run is below the declared minimum.

## Source and nuisance review

The source-provenance record still has null source identifier, URL/citation, retrieval date, original filename/checksum, cadence, and observation metadata. The source must be identified and verified against the actual original file before any further scientific use. The possible shared solar-cycle structure with the sunspot primary domain also requires a documented nuisance-dependence review.

## Decision

Do not count this dataset as replication. Do not interpolate, silently remove intervals, concatenate separated segments, or change the minimum length to make it pass. Any alternative handling would define a new analysis protocol and must be justified and frozen before examining the endpoint result; it cannot retroactively convert this dataset into independent confirmation.

Reconsideration requires all of the following, in order:

1. Identify the original source and verify the downloaded file's checksum and license/citation.
2. Preserve timestamps in the analysis input and document timezone, cadence, duplicates, missing intervals, and all exclusions.
3. Establish a defensible sampling/continuity rule and confirm that a valid segment meets the already-declared replication minimum; if it does not, reject this candidate for the current protocol.
4. Assess solar-cycle/common-nuisance dependence against the primary domain.
5. Apply the same prospectively frozen endpoint and null protocol, if and only if the candidate remains eligible.

This document grants no replication credit, claim support, or promotion authority.
