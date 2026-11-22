# HCM Publications — Paper-by-Paper Identity and Closure Audit

**Audit date:** 2026-11-22  
**Scope:** Papers 01–10, repository Markdown sources, supplied ten-paper ZIP, three separately supplied working PDFs, publication registry, and owner-supplied metadata.  
**Overall status:** `ARCHIVAL_RECONCILIATION_PARTIAL / SCHOLARLY_REVIEW_NOT_ESTABLISHED / EMPIRICAL_VALIDATION_NOT_CLAIMED`

## 1. Executive disposition

The supplied `HCM_Zenodo_10_Papers(1).zip` passes ZIP integrity testing. It contains ten paper PDFs and `README.pdf` (11 entries). SHA-256:

`b75f37026ee3cdc04ea79a671d166dfc7ac1b1227a7ee4a72a7f29a98b075562`

All ten candidate PDF MD5 values match the current repository publication registry. For Papers 02–10, those values also match the owner-supplied JSON metadata capture. This establishes local candidate-to-registry agreement; it does **not** establish direct binary identity with the files currently served by Zenodo because the published PDF binaries were not directly downloaded in this review.

The three separately uploaded working PDFs for Papers 01, 08, and 10 are byte-distinct from the corresponding ZIP candidates. Their normalized extracted text is identical to the ZIP candidates, but their byte-level hashes differ. Preserve both copies until the exact Zenodo binaries are downloaded and verified.

The current repository Markdown source for each paper begins with a disclaimer that it is a conceptual manuscript, not an empirical finding, and that the computational hypothesis remains under investigation. The supplied published PDFs do not contain that same current disclaimer in their extracted text. All ten PDFs lack a references/bibliography section and have no author value in their PDF metadata fields. The papers should therefore be represented as conceptual/theoretical publications, not peer-reviewed empirical demonstrations.

**No paper is classified as empirically validated or independently peer reviewed by this audit.** Publication existence, manuscript identity, peer review, computational reproducibility, and empirical validation remain separate states.

## 2. Binary and metadata evidence

### Candidate PDFs in supplied ZIP

| Paper | Candidate PDF filename | Bytes | Candidate MD5 | Version DOI |
|---|---|---:|---|---|
| 01 | `HCM_Paper_01_Presence_Without_Demand.pdf` | 70,764 | `a240e99737d9d29c44c7f2fc161ca8b1` | `10.5281/zenodo.18148140` |
| 02 | `HCM_Paper_2_Autonomy_Without_Demand.pdf` | 99,264 | `045ce4aec6077eb238fdff0c4a1bc8f3` | `10.5281/zenodo.18168287` |
| 03 | `HCM_Paper_03_When_Capability_Does_Not_Become_Action.pdf` | 101,190 | `2772be59d4f02e4e64f6055ec69f4673` | `10.5281/zenodo.18168932` |
| 04 | `HCM_Paper_04_When_Capability_Does_Not_Become_Action.pdf` | 80,328 | `e8c9ab7dc6c2ce315562c3948b47c506` | `10.5281/zenodo.18169421` |
| 05 | `HCM_Paper_05_The_Field_That_Does_Not_Ask_to_Operate.pdf` | 172,876 | `86f0cb907abe28f36070492a351fb0fd` | `10.5281/zenodo.18177283` |
| 06 | `HCM_Paper_06_Systems_That_Survive_Being_Left_Alone.pdf` | 233,504 | `7a889f75d727165437e5e7797d372f83` | `10.5281/zenodo.18181050` |
| 07 | `HCM_Paper_07_When_the_System_Does_Not_Answer.pdf` | 117,951 | `197714d5b6e5548fac66fb1b4e41fc8d` | `10.5281/zenodo.18182089` |
| 08 | `HCM_Paper_08_When_Measurement_Approaches_the_Thresholdes.pdf` | 353,625 | `93821672f0ce53bd98f9060c1909da4c` | `10.5281/zenodo.18190317` |
| 09 | `HCM_Paper_09_When_the_System_Does_Not_Answer.pdf` | 124,010 | `73b9f42974b4a6190a4f97486ebe5cae` | `10.5281/zenodo.18193434` |
| 10 | `HCM_Paper_10_Application_Without_Extraction.pdf` | 208,622 | `cb6cf6515cc37f4d83c9e13ae21a0cb5` | `10.5281/zenodo.18214787` |

Concept DOIs remain separately recorded in the repository registry. Papers 07 and 09 have distinct version DOIs, concept DOIs, filenames, sizes, and MD5 values; do not merge them.

### Separately uploaded working PDFs

| Paper | Working bytes | Working MD5 | ZIP candidate MD5 | Normalized extracted text |
|---|---:|---|---|---|
| 01 | 70,356 | `24a27ca6b33a0ada641c1f96ed50ab63` | `a240e99737d9d29c44c7f2fc161ca8b1` | Identical |
| 08 | 340,399 | `a69b11345fb4d83abe5bf3e58d9d10ff` | `93821672f0ce53bd98f9060c1909da4c` | Identical |
| 10 | 196,618 | `62ef82c7c2efeea2dc10a20366dfadf5` | `cb6cf6515cc37f4d83c9e13ae21a0cb5` | Identical |

The working PDFs also have different SHA-256 values from the ZIP candidates. No copy is designated as the Zenodo binary solely from its filename.

### Metadata capture boundary

Owner-supplied JSON for Papers 02–10 reports `is_published=true`, `is_draft=false`, public record/file access, `access_status=open`, `embargo.active=false`, and `is_deleted=false`. This is classified as `OWNER_SUPPLIED_API_JSON`. Direct API retrieval and direct published-PDF download were not completed here; previous attempts returned `Cache miss`, which is not evidence of record absence or deletion.

Paper 01 is not part of the new Papers 02–10 JSON capture. Its current DOI, file size, and MD5 are recorded in the repository registry; its published-PDF SHA-256 remains pending.

## 3. Paper-by-paper content audit

Page counts were obtained by parsing the supplied ZIP PDFs. The current Markdown source for each paper carries the conceptual-manuscript disclaimer; the supplied PDFs do not carry that same disclaimer in extracted text.

| Paper | Pages | Published registry title / topic | Content-level finding | Current closure status |
|---|---:|---|---|---|
| 01 | 7 | **Hybrid Consciousness Model (HCM): Presence Without Demand** — presence, allowance, non-demand | Foundational conceptual statement. PDF explicitly says it provides no empirical validation, benchmarks, or experimental results. No references section; PDF metadata author blank. | `CONCEPTUAL_SCOPE_CLEAR; BINARY_VERIFICATION_PENDING` |
| 02 | 8 | **Autonomy Without Demand: Observations from a Permission-Based System Architecture** | Conceptual/observational discussion; no reproducible observation protocol, dataset, or external case record accompanies the observation. | `CONCEPTUAL_ONLY; OBSERVATION_METHOD_NOT_ESTABLISHED` |
| 03 | 8 | **When Capability Does Not Become Action: On Silent Presence in Technically Complete Systems** | Describes an “observed state” but supplies no reproducible system identity, measurement protocol, or audit log for that observation. | `CONCEPTUAL_ONLY; OBSERVATION_EVIDENCE_NOT_ESTABLISHED` |
| 04 | 7 | **When Capability Does Not Become Action: Stabilized Potential and the Absence of Internal Gradient** | Repository manuscript and PDF are titled **The Silent Assumption of Action**; PDF body begins with that heading. Zenodo registry title is materially different. | `TITLE_AND_MANUSCRIPT_ASSOCIATION_OPEN` |
| 05 | 14 | **The Field That Does Not Ask to Operate: Pre-Operational Coherence as a Structural Property of Hybrid Conscious Systems** | PDF heading is **Pre-Operational Coherence as a Structural Property of Hybrid Conscious System**. “Field” and “structural property” need boundaries so they are not mistaken for a measured physical field or established empirical property. | `CONCEPTUAL_ONLY; TERM_BOUNDARIES_NEED_CLARIFICATION` |
| 06 | 19 | **Systems That Survive Being Left Alone: Structural Longevity Through Non-Dependence in Hybrid Conscious Architectures** | Conceptual design argument; “survival” and “longevity” are not backed by a specified duration, stress test, failure criterion, or longitudinal dataset. | `CONCEPTUAL_ONLY; LONGEVITY_EVIDENCE_NOT_ESTABLISHED` |
| 07 | 7 | **When the System Does Not Answer: Observer Drift in Hybrid Conscious Architectures** | PDF/source title is **Observer Drift in Hybrid Conscious Architectures**. Distinct from Paper 09 despite shared title. | `DISTINCT_RECORD; TITLE_COLLISION_WITH_09` |
| 08 | 33 | **When Measurement Approaches the Threshold: Formalism Without Control in Hybrid Conscious Architectures** | PDF heading and Markdown title are **Formalism Without Control in Hybrid Conscious Architectures**. Zenodo title says **When Measurement Approaches the Threshold**; filename spells `Thresholdes`. “Threshold” is not operationalized as a measurable boundary/test criterion. | `TITLE_ASSOCIATION_OPEN; THRESHOLD_NOT_OPERATIONALIZED` |
| 09 | 9 | **When the System Does Not Answer: Observer Drift in Hybrid Conscious Architectures** | Same registry title as 07 but distinct structure/content. Normalized PDF text comparison gives approximately 4.9% sequence similarity; not duplicates on this comparison. Preserve separate DOI/record. | `DISTINCT_RECORD; TITLE_COLLISION_WITH_07` |
| 10 | 16 | **Application Without Extraction: Reframing Application as Presence Within the Hybrid Consciousness Model** | PDF heading is **Reframing Application as Presence Within the Hybrid Consciousness Model**. Broad design/economic implications are not accompanied by an implementation case study or measured economic evaluation. | `CONCEPTUAL_ONLY; APPLICATION_EVIDENCE_NOT_ESTABLISHED` |

## 4. Common scholarly-quality findings

Across all ten supplied PDFs:

- no `References` or `Bibliography` section was detected in extracted text;
- no DOI citation strings were detected;
- PDF metadata author fields are blank;
- the PDFs do not include the current Markdown disclaimer that labels them conceptual rather than empirical;
- the documents are conceptual/theoretical arguments, not empirical reports with reproducible methods, datasets, and statistical results.

These findings do not invalidate the existence of published records. They limit what the papers can support and how they should be described.

Before journal submission or a new scholarly version, each manuscript needs a paper-specific editorial pass to:

1. define key constructs and distinguish metaphorical, architectural, phenomenological, and physical meanings;
2. add a literature review and verifiable citations to relevant prior work;
3. state assumptions, propositions, scope limits, counterexamples, and what would count against the proposal;
4. supply a reproducible observation protocol whenever it uses words such as “observed,” “survival,” “stability,” or “structural property” empirically;
5. add author/title/DOI metadata to PDF properties and align title, subtitle, abstract, keywords, filename, Markdown source, and Zenodo record;
6. add empirical methods/results only when actual data and analyses exist, without importing results from the separate computational repository as proof of conceptual claims.

## 5. Required title and identity reconciliation

- **Paper 04:** preserve published DOI and metadata as historical facts. Resolve source/PDF title **The Silent Assumption of Action** versus Zenodo title **When Capability Does Not Become Action: Stabilized Potential and the Absence of Internal Gradient** using direct record/PDF retrieval and a documented editorial decision. Do not silently rename the existing record.
- **Paper 08:** preserve the observed PDF/Markdown title **Formalism Without Control in Hybrid Conscious Architectures**. Reconcile it against Zenodo title **When Measurement Approaches the Threshold** and filename spelling `Thresholdes`. Do not silently rewrite the registry.
- **Papers 07 and 09:** preserve separate DOIs and records. The shared title is a catalog collision, not proof of duplicate content. A future version may use distinct subtitles, but only through a documented version update.
- **Papers 01, 08, and 10:** preserve the separately uploaded byte-distinct working PDFs alongside the ZIP candidates. Download the published Zenodo PDF for each and compare byte size, MD5, and SHA-256 before designating an authoritative binary.

## 6. Closure matrix

| Closure dimension | Result |
|---|---|
| Ten local candidate PDFs readable and ZIP integrity passed | `CLOSED_ADMINISTRATIVELY` |
| Candidate PDF MD5 compared with repository registry | `PASS_SCOPE_LIMITED` for all ten |
| Direct Zenodo published-PDF binary verification | `PENDING` for all ten |
| Owner-supplied Zenodo metadata capture | `AVAILABLE` for Papers 02–10; Paper 01 relies on repository registry in this capture |
| Manuscript/title association | `OPEN` for Papers 04 and 08; title collision for 07/09 |
| PDF author metadata | `OPEN` for all ten (author field blank) |
| References/related-work apparatus | `OPEN` for all ten |
| Independent peer review of these ten papers | `NOT_ESTABLISHED` |
| Empirical validation of HCM consciousness/causal claims | `NOT_ESTABLISHED` |
| Support for the separate computational spectral hypothesis | `NOT_ESTABLISHED`; governed by its own validation protocol |

## 7. Final disposition and next actions

The ten records may remain preserved as the first conceptual HCM publication series. Their archival existence and local candidate checksums can be recorded; their scientific scope must remain explicitly conceptual. Do not represent them as empirically validated, peer reviewed, or as evidence that the separate computational hypothesis passed its tests.

Next steps:

1. Obtain the exact published PDF binary directly from each Zenodo version record and record retrieval date, byte size, MD5, and SHA-256.
2. Resolve Paper 04 and Paper 08 title/source associations without overwriting historical metadata.
3. Preserve Papers 07 and 09 as distinct records; use distinct subtitles only through a deliberate future-version decision.
4. Complete a citation and conceptual-definition review of all ten manuscripts before journal submission or a new version.
5. Keep current Zenodo records unchanged until the owner approves a specific, documented version update.

No new Zenodo version, metadata edit, deletion, or replacement is authorized by this audit.
