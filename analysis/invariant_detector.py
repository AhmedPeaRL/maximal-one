import os
import pandas as pd
import json
import numpy as np

HISTORY="data/invariant_history.csv"
OUT="artifacts/invariant_patterns.json"

if not os.path.exists(HISTORY):
    exit()

df=pd.read_csv(HISTORY)

def cluster(values,tol=0.1):
    groups=[]
    for v in values:
        placed=False
        for g in groups:
            if abs(np.mean(g)-v)<tol:
                g.append(v)
                placed=True
                break
        if not placed:
            groups.append([v])
    return groups

alpha_groups=cluster(df["spectral_alpha"].values)
dim_groups=cluster(df["attractor_dim"].values)

result={
    "alpha_clusters":[{"mean":float(np.mean(g)),"count":len(g)} for g in alpha_groups],
    "dimension_clusters":[{"mean":float(np.mean(g)),"count":len(g)} for g in dim_groups]
}

with open(OUT,"w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
