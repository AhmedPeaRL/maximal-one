import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist

def correlation_dimension(x, r_vals=None):

    x = np.asarray(x)

    if r_vals is None:
        r_vals = np.logspace(-3, 0, 20)

    dists = pdist(x.reshape(-1,1))

    C = []

    for r in r_vals:
        C.append(np.mean(dists < r))

    C = np.array(C)

    log_r = np.log(r_vals)
    log_C = np.log(C + 1e-12)

    slope = np.polyfit(log_r, log_C, 1)[0]

    return slope


def simple_lyapunov(x):

    x = np.asarray(x)

    diffs = np.abs(np.diff(x))

    growth = np.log(diffs[1:] / (diffs[:-1] + 1e-12) + 1e-12)

    return np.mean(growth)


def recurrence_entropy(x, bins=50):

    hist,_ = np.histogram(x, bins=bins, density=True)

    p = hist / np.sum(hist)

    p = p[p>0]

    return -np.sum(p*np.log(p))


def compute_metrics(series):

    return {
        "corr_dimension": correlation_dimension(series),
        "lyapunov_proxy": simple_lyapunov(series),
        "recurrence_entropy": recurrence_entropy(series)
    }
