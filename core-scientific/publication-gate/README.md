# Publication Gate — Scientific Integrity Layer

This layer is the deterministic validator of the system.

It enforces mathematical coherence before any publication artifact is produced.

## What it validates

1. Empirical convergence  
   Relative error must remain below 1%.

2. Non-zero variance  
   The system must exhibit dynamic spread.

3. Presence of chaotic regimes  
   At least one positive Lyapunov exponent region must exist.

4. Presence of stable regimes  
   At least one negative Lyapunov exponent region must exist.

5. Sensitivity boundedness  
   Drift across perturbed initial conditions must remain below 0.05.

If any of these fail, the system halts immediately.

## Output

A structured `report.json` file containing:

- empirical diagnostics
- sensitivity diagnostics
- bifurcation scan results
- integrity confirmation flag

Status values:
- `SELF_CONSISTENT`
- `READY_FOR_PUBLICATION`

This gate guarantees that the engine is not numerically unstable,
not trivially deterministic,
and not falsely chaotic.

It enforces balanced dynamical truth.
