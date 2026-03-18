import json
import numpy as np
import pathlib

ART = pathlib.Path("artifacts")

# مثال: تحويل نتائج real_world_predictive_test إلى time series

data_path = ART / "predictive_test.json"

if not data_path.exists():
    print("No predictive data")
    exit(0)

data = json.loads(data_path.read_text())

# افتراض وجود residuals
residuals = data.get("residuals", [])

if len(residuals) < 10:
    print("Not enough data")
    exit(0)

real_series = np.array(residuals)

# model approximation (placeholder)
model_series = real_series * 0.9

ART.mkdir(exist_ok=True)

(ART / "real_series.json").write_text(json.dumps(real_series.tolist()))
(ART / "model_series.json").write_text(json.dumps(model_series.tolist()))

print("Real temporal series built")
