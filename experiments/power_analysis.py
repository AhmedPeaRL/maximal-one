import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp
import json

DATA_PATH = "../data/multi_seed_results.csv"
REFERENCE = 0.5

def main():
    df = pd.read_csv(DATA_PATH)
    alphas = df["mu_boot"].values

    t_stat, p_value = ttest_1samp(alphas, REFERENCE)

    result = {
        "mean_alpha": float(np.mean(alphas)),
        "std_alpha": float(np.std(alphas)),
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "reference": REFERENCE
    }

    with open("../data/power_result.json","w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()
