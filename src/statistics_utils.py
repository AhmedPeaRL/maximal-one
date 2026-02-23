import numpy as np
from statsmodels.stats.multitest import multipletests

def compute_zscores(values):
    mean = np.mean(values)
    std = np.std(values)
    if std == 0:
        return np.zeros_like(values)
    return (values - mean) / std

def bonferroni_correction(p_values, alpha=0.05):
    reject, corrected_pvals, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')
    return reject, corrected_pvals

def fdr_correction(p_values, alpha=0.05):
    reject, corrected_pvals, _, _ = multipletests(p_values, alpha=alpha, method='fdr_bh')
    return reject, corrected_pvals
