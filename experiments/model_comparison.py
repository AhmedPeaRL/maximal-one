import numpy as np
import pandas as pd
from scipy import stats

def compute_bic(log_likelihood, n, k):
    return k * np.log(n) - 2 * log_likelihood

def random_walk_model(x):
    residuals = np.diff(x)
    sigma = np.std(residuals)
    ll = np.sum(stats.norm.logpdf(residuals, 0, sigma))
    return ll, 1

def ar1_model(x):
    y = x[1:]
    X = x[:-1]
    beta = np.dot(X, y) / np.dot(X, X)
    residuals = y - beta * X
    sigma = np.std(residuals)
    ll = np.sum(stats.norm.logpdf(residuals, 0, sigma))
    return ll, 2

def hcm_model(x):
    trend = np.mean(np.diff(x))
    residuals = np.diff(x) - trend
    sigma = np.std(residuals)
    ll = np.sum(stats.norm.logpdf(residuals, 0, sigma))
    return ll, 2

def main():
    path = "../data/multi_seed_results.csv"

    try:
        df = pd.read_csv(path)
    except:
        raise RuntimeError("Dataset missing or corrupted")

    if "spectral_exponent" not in df.columns:
        raise ValueError("spectral_exponent column missing")

    x = df["spectral_exponent"].values  # ✅ FIX

    n = len(x)

    ll_rw, k_rw = random_walk_model(x)
    ll_ar, k_ar = ar1_model(x)
    ll_hcm, k_hcm = hcm_model(x)

    bic_rw = compute_bic(ll_rw, n, k_rw)
    bic_ar = compute_bic(ll_ar, n, k_ar)
    bic_hcm = compute_bic(ll_hcm, n, k_hcm)

    print("BIC Random Walk:", bic_rw)
    print("BIC AR(1):", bic_ar)
    print("BIC HCM:", bic_hcm)
    print("ΔBIC (AR - HCM):", bic_ar - bic_hcm)
    print("ΔBIC (RW - HCM):", bic_rw - bic_hcm)

if __name__ == "__main__":
    main()
