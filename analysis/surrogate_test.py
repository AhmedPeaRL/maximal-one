import numpy as np
import pandas as pd
from scipy.signal import welch
import json
import os

DATA_DIR = "real-data"

def spectral_alpha(x):

    f,P = welch(x,nperseg=min(256,len(x)))

    f = f[1:]
    P = P[1:]

    logf = np.log(f)
    logp = np.log(P + 1e-12)

    a,b = np.polyfit(logf,logp,1)

    return -a


results = {}

for file in os.listdir(DATA_DIR):

    if not file.endswith(".csv"):
        continue

    path = os.path.join(DATA_DIR,file)

    try:
        df = pd.read_csv(path)
    except:
        continue

    num = df.select_dtypes(include=[np.number])

    if num.shape[1] == 0:
        continue

    x = num.iloc[:,0].dropna().values

    if len(x) < 200:
        continue

    real_alpha = spectral_alpha(x)

    shuffled = np.random.permutation(x)

    surrogate_alpha = spectral_alpha(shuffled)

    results[file] = {
        "real_alpha": float(real_alpha),
        "surrogate_alpha": float(surrogate_alpha),
        "difference": float(real_alpha - surrogate_alpha)
    }

os.makedirs("artifacts",exist_ok=True)

with open("artifacts/surrogate_test.json","w") as f:
    json.dump(results,f,indent=2)

print(json.dumps(results,indent=2))
