import json
import numpy as np
import pathlib

ART = pathlib.Path("artifacts")

# logistic map (ecology proxy)
r = 3.9
x = 0.2

series = []
for _ in range(5000):
    x = r * x * (1 - x)
    series.append(x)

real = np.array(series)
model = np.random.permutation(real)

ART.mkdir(exist_ok=True)

(ART / "eco_real.json").write_text(json.dumps(real.tolist()))
(ART / "eco_model.json").write_text(json.dumps(model.tolist()))

print("Ecology series generated:", len(real))
