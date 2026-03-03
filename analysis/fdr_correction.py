import numpy as np
from statsmodels.stats.multitest import multipletests

p_values = np.loadtxt("data/p_values_log.txt")

rejected, corrected, _, _ = multipletests(p_values, method='fdr_bh')

print("Rejected after FDR:", rejected.sum())
