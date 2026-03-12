import json
import numpy as np
from pathlib import Path

IN = "artifacts/universal_invariants.json"
OUT = "artifacts/invariant_field_report.json"


def main():

    if not Path(IN).exists():
        print("no invariant file")
        return

    data = json.load(open(IN))

    dims = [d["attractor_dim"] for d in data if d["attractor_dim"]]

    alphas = [d["spectral_alpha"] for d in data]

    ent = [d["entropy"] for d in data]

    report = {

        "datasets":len(data),

        "attractor_dimension":{
            "mean":float(np.mean(dims)),
            "std":float(np.std(dims))
        },

        "spectral_alpha":{
            "mean":float(np.mean(alphas)),
            "std":float(np.std(alphas))
        },

        "entropy":{
            "mean":float(np.mean(ent)),
            "std":float(np.std(ent))
        }

    }

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:

        json.dump(report,f,indent=2)

    print("Invariant field analyzed")


if __name__ == "__main__":
    main()
