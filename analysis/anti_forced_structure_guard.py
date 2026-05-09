import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

DATASET = "real-data/white_noise.csv"

df = pd.read_csv(DATASET)

x = df.iloc[:, 0].values.astype(float)

alpha = estimate_alpha(x)

print("White noise alpha:", alpha)

if alpha > 1.5:
    raise SystemExit(
        "❌ artificial structure inflation detected"
    )

print("✅ no forced structure detected")
