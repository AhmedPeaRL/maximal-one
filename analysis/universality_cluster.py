import json
import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path

FEATURE_FILE = "artifacts/spectral_features.json"

def load_features():

    if not Path(FEATURE_FILE).exists():
        return None

    with open(FEATURE_FILE) as f:
        return json.load(f)

def cluster_systems(features):

    names=[]
    X=[]

    for k,v in features.items():

        if "alpha" not in v:
            continue

        names.append(k)
        X.append([v["alpha"], v.get("hurst",0), v.get("lyapunov",0)])

    X=np.array(X)

    if len(X)<5:
        return None

    kmeans=KMeans(n_clusters=3,random_state=42)
    labels=kmeans.fit_predict(X)

    clusters={}

    for name,l in zip(names,labels):
        clusters.setdefault(int(l),[]).append(name)

    return clusters

def main():

    features=load_features()

    if features is None:
        print("No features available")
        return

    clusters=cluster_systems(features)

    if clusters is None:
        print("Not enough systems")
        return

    Path("artifacts").mkdir(exist_ok=True)

    with open("artifacts/universality_clusters.json","w") as f:
        json.dump(clusters,f,indent=2)

    print(json.dumps(clusters,indent=2))

if __name__=="__main__":
    main()
