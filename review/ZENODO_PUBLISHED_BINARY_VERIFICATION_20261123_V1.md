# Zenodo Published Binary Verification Addendum — V1

- **Evidence date:** 2026-11-23
- **Repository:** `AhmedPeaRL/maximal-one`
- **Target branch for this documentation:** `review/type1-v4-remediation`
- **Main branch:** `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- **Review branch at verification:** `5397113032232f2e5c9ddeb4b776509d9a4b5f86`
- **Disposition:** `REVIEW_ONLY / BINARY_IDENTITY_PASS_SCOPE_LIMITED / NO_WORKFLOW_AUTHORIZED`

## 1. Scope and evidence classification

This document records a bounded publication-file identity check. It does not freeze the Type-I protocol, authorize calibration or confirmatory execution, establish scientific validity, establish peer review, or support promotion of scientific claims.

Two evidence streams were compared:

1. **Owner-executed Termux verification.** The repository owner supplied the complete output from `zenodo_verify.py`, executed locally in Termux. The output reports actual downloads, byte counts, PDF signatures, MD5, SHA-256, Zenodo metadata checksum comparisons, and Registry MD5 comparisons.
2. **Assistant-side archive verification.** The Library file `Current Evidence/Zenodo_HCM_Published_Papers.zip` was materialized and inspected locally. Its ZIP integrity test passed (`testzip()` returned `None`). The archive contains ten paper PDFs plus one `README.pdf`. All eleven extracted files had valid `%PDF-` signatures. Their sizes, MD5 values, and SHA-256 values were recomputed and matched the owner-supplied Termux output exactly.

**Important limitation:** the assistant environment could not independently download the PDFs from Zenodo during this review. The direct-download execution is therefore classified as owner-executed evidence, while the independent recomputation is against the separately stored Library ZIP. The script source and raw execution transcript were not separately uploaded with cryptographic digests; their hashes are not asserted here.

## 2. Library archive identity

- Library path: `Hybrid Consciousness Model - HCM/Current Evidence/Zenodo_HCM_Published_Papers.zip`
- Archive size: `1,115,283` bytes
- Archive SHA-256: `c025b132da7f9c0727e9646cefb0ba0c2aabca096955b4cbbf51875579a0adf3`
- ZIP entries: `11`
- Files: `11`
- Uncompressed size: `1,620,811` bytes
- ZIP integrity: `PASS` (`testzip() == None`)

The archive contains Papers 01–10 and `README.pdf`. All eleven files' locally recomputed SHA-256 and MD5 values matched the Termux output supplied by the owner.

## 3. Published paper manifest

All ten paper PDFs report:
- downloaded byte count equal to Zenodo's declared size;
- a valid `%PDF-` signature;
- actual MD5 equal to Zenodo's file checksum;
- actual MD5 equal to the Registry MD5;
- actual SHA-256 equal to the assistant-side recomputation from the Library archive.

| Paper | Zenodo record | DOI | File | Bytes | MD5 | SHA-256 |
|---|---:|---|---|---:|---|---|
| 01 | 18148140 | [https://doi.org/10.5281/zenodo.18148140](https://doi.org/10.5281/zenodo.18148140) | `HCM_Paper_01_Presence_Without_Demand.pdf` | 70,764 | `a240e99737d9d29c44c7f2fc161ca8b1` | `0afdc65873debb2f50fc9a20864957ae8cc541e6d4926a8ae86d2cf340e75162` |
| 02 | 18168287 | [https://doi.org/10.5281/zenodo.18168287](https://doi.org/10.5281/zenodo.18168287) | `HCM_Paper_2_Autonomy_Without_Demand.pdf` | 99,264 | `045ce4aec6077eb238fdff0c4a1bc8f3` | `85528a4977effdd3a82b7e051b02992563e33a3fc830f27294a46890b301bb9e` |
| 03 | 18168932 | [https://doi.org/10.5281/zenodo.18168932](https://doi.org/10.5281/zenodo.18168932) | `HCM_Paper_03_When_Capability_Does_Not_Become_Action.pdf` | 101,190 | `2772be59d4f02e4e64f6055ec69f4673` | `a7ca8c87cd9ebcf8640e4113f3fd7835ff351d8049cfa8b10c30b53843d14f7d` |
| 04 | 18169421 | [https://doi.org/10.5281/zenodo.18169421](https://doi.org/10.5281/zenodo.18169421) | `HCM_Paper_04_When_Capability_Does_Not_Become_Action.pdf` | 80,328 | `e8c9ab7dc6c2ce315562c3948b47c506` | `2f6e63e837c49ea2943b199be927c7abfc7387b08183962551a42cca5fa6101a` |
| 05 | 18177283 | [https://doi.org/10.5281/zenodo.18177283](https://doi.org/10.5281/zenodo.18177283) | `HCM_Paper_05_The_Field_That_Does_Not_Ask_to_Operate.pdf` | 172,876 | `86f0cb907abe28f36070492a351fb0fd` | `b1f1964a410566befa7fe3a6601bb6706bee3776280a56c7f46bc273136bc905` |
| 06 | 18181050 | [https://doi.org/10.5281/zenodo.18181050](https://doi.org/10.5281/zenodo.18181050) | `HCM_Paper_06_Systems_That_Survive_Being_Left_Alone.pdf` | 233,504 | `7a889f75d727165437e5e7797d372f83` | `9bb802f6c839ebb94364ca451b7a1c425131e34fd6741e3413fe83149cdc8406` |
| 07 | 18182089 | [https://doi.org/10.5281/zenodo.18182089](https://doi.org/10.5281/zenodo.18182089) | `HCM_Paper_07_When_the_System_Does_Not_Answer.pdf` | 117,951 | `197714d5b6e5548fac66fb1b4e41fc8d` | `9b61ac0996cede283c9c4fdec0faed052e94a4177be0f2909e1609bda5ba0e73` |
| 08 | 18190317 | [https://doi.org/10.5281/zenodo.18190317](https://doi.org/10.5281/zenodo.18190317) | `HCM_Paper_08_When_Measurement_Approaches_the_Thresholdes.pdf` | 353,625 | `93821672f0ce53bd98f9060c1909da4c` | `07bf4d86d6e1e4f0a447f3c9f947d1128fcd271ccd7e171d709fe9b188b167eb` |
| 09 | 18193434 | [https://doi.org/10.5281/zenodo.18193434](https://doi.org/10.5281/zenodo.18193434) | `HCM_Paper_09_When_the_System_Does_Not_Answer.pdf` | 124,010 | `73b9f42974b4a6190a4f97486ebe5cae` | `fc46df04cc95ddd8187acde93113a2ff132f9762a0b0aef4e4bbb558dc0e0ca1` |
| 10 | 18214787 | [https://doi.org/10.5281/zenodo.18214787](https://doi.org/10.5281/zenodo.18214787) | `HCM_Paper_10_Application_Without_Extraction.pdf` | 208,622 | `cb6cf6515cc37f4d83c9e13ae21a0cb5` | `63e541a3ab3872989745e622fefb33f99ac11c9032c36a924e551d003e20196e` |

## 4. Additional README file

`README.pdf` is an additional file in Paper 01's Zenodo record. It is not an eleventh research paper and has no Registry paper-MD5 value to compare.

- Size: `58,677` bytes
- MD5: `adaa0b0a00581ec5eee46e55cc73f0ca`
- SHA-256: `e826ff0e3a64994470181f3ba4ef8fed604ee3d708a6f6158cecf3ba6e8e8d1e`
- PDF signature: valid
- Zenodo binary checksum: match
- Registry MD5: `NOT_APPLICABLE` (expected; this is README.pdf, not the paper PDF)

## 5. Paper title and filename observations

The following are presentation/metadata observations, not binary-integrity failures:

- **Paper 04:** the PDF text begins with `1. The Silent Assumption of Action`; it does not print the full Zenodo record title as a title page. The body explicitly discusses stabilized capability and an `internal gradient`, which is substantively consistent with the record title. Classify the record-to-content association as `CONTENT_CONSISTENT / FULL_TITLE_NOT_PRINTED_IN_PDF`; do not alter the DOI record or PDF on this evidence alone.
- **Paper 08:** the PDF begins with `Formalism Without Control in Hybrid Conscious Architectures`, matching the subtitle portion of the Zenodo record title. The filename contains `Thresholdes` while the record title uses `Threshold`. Classify this as `FILENAME_TYPO / CONTENT_ASSOCIATION_SUPPORTED`; it does not affect the hash.
- **Papers 07 and 09:** they have the same displayed record title but are separate Zenodo records, have different file sizes, and have different MD5/SHA-256 values. Preserve both as distinct records; do not merge them.

## 6. Working manuscript is not the published binary

The Library's `Working Manuscripts - Binary Identity Pending/HCM_Paper_01_Presence_Without_Demand.pdf` was separately materialized and hashed:

- Working manuscript size: `70,356` bytes
- Working manuscript MD5: `24a27ca6b33a0ada641c1f96ed50ab63`
- Working manuscript SHA-256: `fb97104ce381683d9721657f3bdd6abe32ce9b2629043b9965826e388724dd29`

The published Paper 01 PDF is `70,764` bytes, MD5 `a240e99737d9d29c44c7f2fc161ca8b1`, SHA-256 `0afdc65873debb2f50fc9a20864957ae8cc541e6d4926a8ae86d2cf340e75162`.

These are different binaries. Preserve the working manuscript and published PDF as separate objects. Do not overwrite, rename, or delete either merely to make their hashes agree.

## 7. Library organization observed during this review

- `Current Evidence/` contains `Zenodo_HCM_Published_Papers.zip` and the Run35/Run36 evidence archives.
- `Zenodo PDF Candidates - Registry MD5 Match/` returned no files in the current listing.
- `Working Manuscripts - Binary Identity Pending/` contains the distinct Paper 01 working manuscript described above.
- `Publications and Provenance/` returned no files in the current listing.

No Library file was moved, replaced, or deleted during this review. The existing ZIP and historical artifacts are preserved.

## 8. Repository and workflow boundary

The observed repository refs at review time were:
- `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation`: `5397113032232f2e5c9ddeb4b776509d9a4b5f86`

The V12 commit remains unchanged and is preserved as historical evidence. Its earlier statement that direct Zenodo binary identity remained open is superseded for the ten paper PDFs by this bounded V1 addendum; V12 itself must not be rewritten.

A GitHub Actions run query filtered to runs created after `2026-11-22T17:11:22Z` returned `total_count=0` at the time of this review. This is a query result, not a claim about workflow enabled/disabled settings.

`NO_WORKFLOW_AUTHORIZED` remains in force. This addendum does not authorize any `.yml` workflow, manual dispatch, automatic run, container build, Type-I calibration, confirmatory analysis, replication, or claim promotion.

Before any future documentation commit to the Review branch, the owner must manually confirm that `Build and Publish Container` (`.github/workflows/build-image.yml`) is disabled. Its current definition has an unfiltered `push` trigger; if enabled, a Review-branch documentation push can start its build job. The publish job is restricted to `main`, but that does not eliminate the build-job trigger risk. Server-side disablement was not independently verified in this review.

## 9. Scientific and review status

- Binary identity of the ten published paper PDFs: `PASS_SCOPE_LIMITED`
- README binary identity: `PASS_SCOPE_LIMITED`
- Scientific validity or empirical confirmation of HCM claims: `NOT_ESTABLISHED`
- Independent peer review of all ten papers: `NOT_ESTABLISHED`
- Type-I protocol freeze: `NOT_FROZEN`
- Formal Type-I calibration: `NOT_AUTHORIZED`
- Confirmatory execution: `NOT_AUTHORIZED`
- Replication: `NOT_AUTHORIZED`
- Claim support and promotion authority: `NOT_ESTABLISHED / NONE`
- Container security: `OPEN`
- Four requested human review reports: `PENDING_INDEPENDENT_REVIEW`

## 10. Required preservation and next actions

1. Preserve V12 unchanged.
2. Preserve the Library ZIP and all eleven extracted file identities.
3. Preserve the distinct Paper 01 working manuscript; do not replace it with the published binary.
4. Upload and retain the exact `zenodo_verify.py` script and raw Termux output in the Library so future reviewers can inspect the executable and transcript. No script hash is asserted until the script bytes are supplied.
5. Add this addendum and the companion SHA-256SUMS file to the Review branch only, **only after manually confirming that `build-image.yml` is disabled**. If disablement cannot be confirmed, do not push a commit.
6. Do not run any workflow as part of this documentation update.
7. Do not modify `main`, workflow YAML, Dockerfile, application code, scientific protocols, datasets, or DOI records.

No global 100% assurance, scientific validation, empirical confirmation, or peer-review closure is claimed.
