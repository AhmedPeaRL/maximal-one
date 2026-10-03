# Diagnostic Null Method Change Log

## Status

DIAGNOSTIC_ONLY

This document records a methodological change in the non-primary diagnostic
null path. It does not establish, strengthen, weaken, or promote the
scientific claim.

---

## Reason for recording

The diagnostic null distribution changed after the diagnostic null
implementation was revised for reproducibility and explicit RNG ownership.

The observed diagnostic distribution must not be interpreted as a scientific
trend until the implementation change is explicitly documented.

---

## Previous implementation characteristics

The previous diagnostic implementation used:

- global NumPy random state;
- `np.random.uniform(...)` for phase generation;
- full complex FFT phase randomization;
- `np.random.shuffle(...)` for block ordering;
- implicit stochastic state rather than a caller-owned RNG.

---

## Current implementation characteristics

The current implementation uses:

- a caller-owned `numpy.random.Generator`;
- deterministic execution for a declared seed;
- `rng.uniform(...)` for phase generation;
- real-valued `rfft/irfft` construction;
- preservation of the DC component;
- preservation of the Nyquist component for even-length series;
- `rng.permutation(...)` for block ordering;
- explicit block size of 50.

---

## Attribution policy

The change in diagnostic null spread MUST NOT be attributed to block
shuffling alone.

Multiple implementation changes occurred simultaneously, including:

1. RNG ownership and random-number consumption;
2. phase-randomization construction;
3. DC/Nyquist treatment;
4. block-order randomization.

Therefore causal attribution of the observed distributional change requires
a controlled side-by-side replay in which the old and new implementations
are evaluated on the same input series under explicitly declared seeds.

---

## Scientific role

This diagnostic path has:

- scientific_claim_authority: false
- promotion_authority: false
- evidence_role: diagnostic_only
- protocol_role: non_primary_diagnostic

It MUST NOT override:

`artifacts/canonical_report.json`

It MUST NOT override:

`core-scientific/strict_claim.json`

It MUST NOT modify the primary stochastic-null result.

---

## Interpretation of the current diagnostic result

A change in diagnostic p-value, null standard deviation, or effect size after
a methodological implementation change is not itself evidence of scientific
improvement.

The correct interpretation is:

"the diagnostic distribution changed after a documented implementation
revision; the direction and magnitude of the change require controlled
attribution before scientific interpretation."

---

## Required future comparison

If attribution becomes scientifically relevant, perform a controlled
comparison containing:

A. previous implementation;
B. current implementation;
C. identical input data;
D. identical declared seed;
E. identical number of diagnostic surrogates;
F. separately recorded phase-randomization and block-shuffle components.

No comparison result may be used as claim-supporting evidence.

---

## Preservation rule

Historical diagnostic results MUST remain preserved.

A new diagnostic result MUST NOT overwrite or silently replace an older
diagnostic result without provenance indicating:

- previous implementation identity;
- new implementation identity;
- declared seed;
- dataset identity;
- number of surrogates;
- methodological differences.

---

## Final epistemic statement

The diagnostic null path is an observational and engineering diagnostic.
It is not the canonical inferential null and has no authority to promote
the scientific claim.
