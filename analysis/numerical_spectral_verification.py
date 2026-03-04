import json
import os
import numpy as np

from spectral_utils import estimate_alpha, generate_white_noise

os.makedirs("artifacts", exist_ok=True)

series = generate_white_noise(5000)
alpha = estimate_alpha(series)

profile = {
    "estimated_alpha": float(alpha),
    "reference_half": 0.5
}

print("==== SPECTRAL PROFILE ====")
print(profile)

with open("artifacts/spectral_profile.json", "w") as f:
    json.dump(profile, f, indent=2)
