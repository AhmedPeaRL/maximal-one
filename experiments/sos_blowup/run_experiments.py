from gap_analysis import compute_gap
from sos_solver import sos_feasible

eps_values = [1e-1, 1e-2, 1e-3, 1e-4]

for eps in eps_values:
    gap = compute_gap(eps)
    print("epsilon:", eps, "gap:", gap)

    for r in [2,3,4,5]:
        status = sos_feasible(eps, r)
        print(" degree", r, "->", status)
