import numpy as np from fbm import FBM from analysis.early_warning_signal import early_warning_indicator
def generate_null(n=5000, hurst=0.5): f = FBM(n=n, hurst=hurst, length=1, method='daviesharte') return f.fbm()
def null_distribution(runs=50): results = [] for _ in range(runs): series = generate_null() r = early_warning_indicator(series) results.append(r["trend_slope"]) return np.array(results)
if name == "main": dist = null_distribution() print("Null mean slope:", np.mean(dist)) print("Null std:", np.std(dist))
