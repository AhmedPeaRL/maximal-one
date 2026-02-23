# Maximal-One Replication Protocol

## Objective

Determine whether the detected spectral spike is:

- Architecture independent (physical phenomenon)
OR
- Runtime / clock / scheduler artifact

No metaphysical claims are made.
All conclusions must survive hostile replication.

---

## Replication Matrix

Each run must record:

- OS
- Architecture
- CPU Model
- Cloud provider (if any)
- Bare metal or virtualized
- Sample size
- Window function
- Normalization mode
- Reboot state

---

## Required Test Variations

1. Sample Size:
   - 1_000_000
   - 500_000
   - 250_000

2. Window Functions:
   - none
   - hann
   - hamming

3. Normalization:
   - raw
   - power_normalized
   - variance_normalized

4. Reboot test:
   - fresh boot
   - warm environment

---

## Criteria for Artifact

The spike is classified as artifact if:

- It disappears under windowing
- It scales non-linearly with sample size
- It appears only on specific architectures
- It shifts frequency between runs

---

## Criteria for Non-Artifact

The spike must:

- Appear across architectures
- Maintain frequency stability
- Maintain proportional scaling
- Survive windowing
- Survive normalization correction

Anything less = artifact.

No exceptions.
