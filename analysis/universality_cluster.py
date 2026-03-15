import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from pathlib import Path

FEATURE_FILE = "artifacts/universality_features.csv"

def load_features():

    if not Path(FEATURE_FILE).exists():
        return None

    df = pd.read_csv(FEATURE_FILE)

    if df.empty:
        return None

    return df

def cluster_systems(df):

    cols = [
        "spectral_alpha",
        "entropy_rate",
        "hurst_exponent",
        "attractor_dimension"
    ]

    df = df.dropna(subset=cols)

    if len(df) < 5:
        return None

    X = df[cols].values

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)

    labels = kmeans.fit_predict(X)

    clusters = {}

    for dataset, label in zip(df["dataset"], labels):
        clusters.setdefault(int(label), []).append(dataset)

    return clusters

def main():

    df = load_features()

    if df is None:
        print("No features available")
        return

    clusters = cluster_systems(df)

    if clusters is None:
        print("Not enough systems")
        return

    Path("artifacts").mkdir(exist_ok=True)

    with open("artifacts/universality_clusters.json","w") as f:
        json.dump(clusters,f,indent=2)

    print("Universality clusters:")
    print(json.dumps(clusters, indent=2))

if __name__ == "__main__":
    main()
