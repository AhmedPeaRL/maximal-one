# Binary Identity and Publication Provenance Policy

Status: ACTIVE_DOCUMENTATION_POLICY
Scope: HCM Zenodo publications

## 1. Purpose

Preserve a verifiable relationship between each published
Zenodo record and the corresponding repository materials.

## 2. Separate identity layers

The following objects are distinct:

- Zenodo record metadata
- Version-specific published PDF
- Concept DOI
- Repository Markdown manuscript
- Locally uploaded working PDF
- Derived text extraction

Similarity of title or extracted text does not establish
binary identity.

## 3. Verification procedure

For each published PDF:

1. Open the version-specific Zenodo DOI.
2. Confirm the record title, creator, version, publication date,
   license, and filename.
3. Download the published PDF directly from Zenodo.
4. Confirm the downloaded byte size.
5. Calculate MD5 and compare it with the record metadata.
6. Calculate SHA-256 and preserve the value in the registry.
7. Record the retrieval date and verification result.

## 4. Status vocabulary

- VERIFIED_BINARY_MATCH
- METADATA_MATCH_BINARY_PENDING
- MD5_MISMATCH
- TITLE_MISMATCH_REVIEW_REQUIRED
- MANUSCRIPT_ASSOCIATION_UNRESOLVED
- RECORD_METADATA_UNVERIFIED
- NOT_ESTABLISHED

No status may be upgraded without supporting evidence.

## 5. Mismatch handling

When a local PDF differs from the published PDF:

- Preserve both files.
- Do not overwrite the published record.
- Do not replace historical hashes.
- Do not infer which file is authoritative from filename alone.
- Retrieve the published binary directly from Zenodo.
- Reconcile the manuscript source separately.

## 6. Scientific interpretation boundary

Conceptual publications are not empirical validation
of computational hypotheses.

The existence of a DOI does not establish:

- empirical confirmation
- independent replication
- causal mechanism
- consciousness
- universality
- predictive validity

Such claims require their own evidence and review.

## 7. Change control

Any correction to publication metadata must retain
the prior value and document the reason for the change.

No publication record may be silently merged,
renamed, or deleted.
