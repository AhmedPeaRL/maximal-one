# SOS Degree Scan (1D Numerical Experiment)

Objective:
Numerically estimate minimal SOS degree required to represent

    f_k(x) = (1 - x^2)^k  on [-1,1]

in the form:

    f_k = σ0 + σ1 (1 - x^2)

where σ0, σ1 are sums of squares with bounded degree.

Method:
- Use Gram matrix parametrization
- Formulate feasibility SDP
- Solve with CVXPY + SCS
- Scan degree d from lower bound upward
- Record minimal feasible d

This is an experimental exploration.
No theoretical claim is made beyond numerical evidence.
