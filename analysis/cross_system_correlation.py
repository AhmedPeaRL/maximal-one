import json
import numpy as np
from pathlib import Path

def corr(a, b):

    if a is None or b is None:
        return None

    a = np.array(a)
    b = np.array(b)

    if a.ndim == 0 or b.ndim == 0:
        return None

    n = min(len(a), len(b))

    if n < 10:
        return None

    a = a[:n]
    b = b[:n]

    if np.std(a) == 0 or np.std(b) == 0:
        return None

    return float(np.corrcoef(a, b)[0,1])

def main():

    path = Path("artifacts/windowed_spectral.json")

    if not path.exists():
        return

    data = json.load(open(path))

    keys = list(data.keys())

    matrix = {}

    for i in range(len(keys)):
        for j in range(i+1,len(keys)):

            a = data[keys[i]].get("alphas", [])
            b = data[keys[j]].get("alphas", [])

            c = corr(a, b)

            if c is None:
                continue

            matrix[f"{keys[i]}__{keys[j]}"] = c

    Path("artifacts").mkdir(exist_ok=True)

    json.dump(matrix,
              open("artifacts/cross_system_corr.json","w"),
              indent=2)

if __name__ == "__main__":
    main()
