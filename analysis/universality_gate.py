import json
import os
import numpy as np

art = "artifacts"

def read_json(name):
    path = os.path.join(art,name)
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path))
    except:
        return None


lyap = read_json("lyapunov.json")
spec = read_json("spectral_verification.json")
scale = read_json("scaling_collapse_engine.json")

passed = True
report = {}

# Lyapunov gate
if lyap and "lyapunov_exp" in lyap:
    report["lyapunov"] = lyap["lyapunov_exp"]
    if lyap["lyapunov_exp"] <= 0:
        passed = False
else:
    passed = False

# Spectral alpha gate
if spec and "alpha" in spec:
    report["spectral_alpha"] = spec["alpha"]
    if not (0.5 < spec["alpha"] < 3.0):
        passed = False
else:
    passed = False

# Scaling collapse gate
if scale and "collapse_error" in scale:
    report["collapse_error"] = scale["collapse_error"]
    if scale["collapse_error"] > 0.2:
        passed = False
else:
    passed = False

report["passed"] = passed

print(json.dumps(report,indent=2))

if not passed:
    exit(1)
