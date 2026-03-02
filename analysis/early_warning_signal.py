import numpy as np import pandas as pd from scipy.stats import zscore from analysis.numerical_spectral_verification import estimate_alpha
def rolling_alpha(series, window=256): alphas = [] for i in range(window, len(series)): segment = series[i-window:i] a = estimate_alpha(segment) alphas.append(a) return np.array(alphas)
def early_warning_indicator(series): alpha_series = rolling_alpha(series) trend = np.polyfit(np.arange(len(alpha_series)), alpha_series, 1)[0] variance = np.var(alpha_series) return { "trend_slope": float(trend), "variance": float(variance), "mean_alpha": float(np.mean(alpha_series)) }
if name == "main": import sys df = pd.read_csv(sys.argv[1]) series = df.iloc[:,0].values result = early_warning_indicator(series) print(result)
