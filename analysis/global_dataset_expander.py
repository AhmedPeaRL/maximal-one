import os
import requests

DATASETS = {
    "sunspots": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv",
    "co2": "https://raw.githubusercontent.com/datasets/co2-ppm/master/data/co2-mm-mlo.csv",
    "temperature": "https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv",
    "ecology": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv"
}

os.makedirs("real-data", exist_ok=True)

for name, url in DATASETS.items():
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            path = f"real-data/{name}.csv"
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"Downloaded {name}")
        else:
            print(f"Failed {name}")
    except Exception as e:
        print("Error", name, e)
