# Long-Term Archival Specification
Status: Temporal Preservation Protocol
Scope: maximal-one

---

## 1. Purpose

Ensure that this repository remains:

- Understandable
- Verifiable
- Reproducible

For decades, independent of infrastructure changes.

---

## 2. Required Archival Components

The following artifacts must always be preserved:

- core-scientific/ source directory
- publication-gate logic
- report.json structure definition
- All tagged releases
- All manifest files
- All policy documents

---

## 3. Archival Format Recommendations

Preferred preservation formats:

- Git repository mirror
- Compressed tar archive (.tar.gz)
- Plain-text export of all .md and .json files

Binary-only storage is discouraged.

---

## 4. Hash Preservation Rule

For every release:

The deterministicArtifactHash must be recorded in:

- Release tag
- Release description
- External archival metadata (if applicable)

---

## 5. Environment Documentation

The following runtime context must be documented:

- Node major version
- Hash algorithm
- OS class (Linux-based)

Exact minor versions are not required,
but major environment class must remain documented.

---

## 6. Interpretive Independence

Future verification must not depend on:

- GitHub availability
- CI runner existence
- External proprietary systems

Verification must be reproducible locally.

---

## 7. Structural Longevity Principle

The repository is designed to outlive:

Infrastructure  
Cloud providers  
CI platforms  

Determinism is the portable invariant.

---

## 8. End-of-Life Condition

If:

- Cryptographic primitives fail
- Runtime ecosystem becomes non-executable
- Verification becomes impossible

The repository remains historically valid,
but operationally retired.

---

End of Long-Term Archival Specification.
