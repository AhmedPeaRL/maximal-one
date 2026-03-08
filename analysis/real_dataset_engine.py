import os
import pandas as pd
import urllib.request
from pathlib import Path

DATASETS = {
    "sunspots": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv",
    "airline_passengers": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
}

DATA_DIR = Path("real-data")
DATA_DIR.mkdir(exist_ok=True)

def download(name, url):
    path = DATA_DIR / f"{name}.csv"
    if path.exists():
        return

    print(f"Downloading {name}")
    urllib.request.urlretrieve(url, path)

def normalize_dataset(path):
    df = pd.read_csv(path)

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return

    series = numeric.iloc[:,0]

    series = (series - series.mean()) / series.std()

    out = path.with_name(path.stem + "_prepared.csv")

    series.to_csv(out, index=False)

def main():
    for name, url in DATASETS.items():
        download(name, url)

    for f in DATA_DIR.glob("*.csv"):
        if "prepared" not in f.name:
            normalize_dataset(f)

if __name__ == "__main__":
    main()
