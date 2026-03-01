import pandas as pd
import numpy as np

real = pd.read_csv("data/multi_seed_results.csv")

real_mean = real["alpha"].mean()

# synthetic null distribution drawn around same mean
null = np.random.normal(loc=real_mean, scale=real["alpha"].std(), size=5000)

kl_div = np.sum(
    real["alpha"].value_counts(normalize=True).values *
    np.log(
        real["alpha"].value_counts(normalize=True).values /
        np.histogram(null, bins=len(real["alpha"].unique()), density=True)[0]
    )
)

print("KL divergence from synthetic null:", kl_div)
