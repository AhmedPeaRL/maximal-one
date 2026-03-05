# HCM Scientific Protocol v1.0

## Objective

To test whether the Hybrid Consciousness Model (HCM) demonstrates
structural predictive superiority over established nonlinear baselines
in chaotic dynamical systems.

---

## Target Phenomenon

Primary benchmark:
Lorenz chaotic attractor (sigma=10, rho=28, beta=8/3)

Secondary benchmarks:
- Real-world chaotic time series (if provided)
- Fractional Brownian Motion (control)
- Null ensemble (randomized baseline)

---

## Baselines

1. AR(p) linear predictor
2. Moving average smoothing
3. Ridge regression on delay embedding
4. Local linear phase space model

All baselines must be deterministic and reproducible.

---

## Core Metrics

1. Mean Squared Error (short horizon)
2. Lyapunov exponent deviation
3. Attractor topology similarity
4. Spectral alpha stability
5. Cross-version deterministic consensus

---

## Breakthrough Criterion

HCM must satisfy at least TWO of the following:

- ≥ 5% relative predictive gain over strongest nonlinear baseline
- ≤ 2% deviation in estimated largest Lyapunov exponent
- Preservation of attractor topology within bounded Hausdorff error
- Statistically significant improvement across ≥ 10 independent seeds

If not achieved, the protocol fails without narrative override.

---

## Reproducibility Requirements

- Fixed seed = 42
- Canonical JSON hashing
- Cross-Node deterministic consensus
- Pinned Python scientific stack
- Environment fingerprint embedded in artifacts

---

## Integrity Clause

No manual override of failing gates.
No metric redefinition post hoc.
No baseline weakening.
No threshold relaxation without protocol revision.

Protocol revisions require version increment.

---

Protocol Version: 1.0
Status: Active
