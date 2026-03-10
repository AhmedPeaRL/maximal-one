import json
import requests
from pathlib import Path

DATASETS = {
    "sunspots": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv",
    "co2": "https://raw.githubusercontent.com/datasets/co2-ppm/master/data/co2-mm-mlo.csv"
}

DATA_DIR = Path("real-data")
DATA_DIR.mkdir(exist_ok=True)

registry = {}

for name, url in DATASETS.items():
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            path = DATA_DIR / f"{name}.csv"
            path.write_bytes(r.content)
            registry[name] = {"status": "downloaded", "url": url}
        else:
            registry[name] = {"status": "failed", "url": url}
    except Exception as e:
        registry[name] = {"status": "error", "message": str(e)}

Path("artifacts").mkdir(exist_ok=True)

with open("artifacts/dataset_registry.json","w") as f:
    json.dump(registry,f,indent=2)

print(json.dumps(registry,indent=2))
