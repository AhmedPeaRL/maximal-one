import numpy as np
import pandas as pd
from scipy.signal import welch
from sklearn.neighbors import NearestNeighbors
from scipy.stats import entropy
import matplotlib.pyplot as plt

def spectral_alpha(series):

    f, Pxx = welch(series, nperseg=256)

    mask = (f > 0)

    f = f[mask]
    Pxx = Pxx[mask]

    logf = np.log10(f)
    logP = np.log10(Pxx)

    slope, _ = np.polyfit(logf, logP, 1)

    return -slope


def entropy_slope(series, window=200):

    entropies = []

    for i in range(len(series) - window):

        segment = series[i:i+window]

        hist, _ = np.histogram(segment, bins=30)

        entropies.append(entropy(hist + 1e-9))

    if len(entropies) < 10:
        return np.nan

    x = np.arange(len(entropies))

    slope, _ = np.polyfit(x, entropies, 1)

    return slope


def correlation_dimension(series, m=3, tau=2):

    N = len(series) - (m-1)*tau

    if N <= 50:
        return np.nan

    embedded = np.zeros((N, m))

    for i in range(m):
        embedded[:, i] = series[i*tau:i*tau+N]

    nbrs = NearestNeighbors(n_neighbors=5).fit(embedded)

    distances, _ = nbrs.kneighbors(embedded)

    r = distances[:,1:]

    log_r = np.log(r.flatten()+1e-10)

    return np.mean(log_r)


def analyze_dataset(name, series):

    alpha = spectral_alpha(series)

    ent = entropy_slope(series)

    dim = correlation_dimension(series)

    return {
        "dataset": name,
        "alpha": alpha,
        "entropy_slope": ent,
        "attractor_dimension": dim
    }


def plot_phase_space(df):

    fig = plt.figure()

    ax = fig.add_subplot(projection='3d')

    ax.scatter(
        df["alpha"],
        df["entropy_slope"],
        df["attractor_dimension"]
    )

    for i,row in df.iterrows():

        ax.text(
            row["alpha"],
            row["entropy_slope"],
            row["attractor_dimension"],
            row["dataset"]
        )

    ax.set_xlabel("spectral alpha")
    ax.set_ylabel("entropy slope")
    ax.set_zlabel("attractor dimension")

    plt.savefig("invariant_phase_space.png")

def save_results(results):

    import json, os

    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/phase_space_invariants.json","w") as f:
        json.dump(results, f, indent=2)

results = []

for dataset in datasets:
    r = analyze_dataset(name, series)
    results.append(r)

save_results(results)
