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

    if not os.path.exists(path):
        print("Dataset missing:", path)
        return

    if os.path.getsize(path) == 0:
        print("Dataset empty:", path)
        return

    try:
        df = pd.read_csv(path)
    except Exception as e:
        print("Failed reading dataset:", path, e)
        return

    if df.shape[1] == 0:
        print("Dataset has no columns:", path)
        return

    # continue processing safely

def main():
    for name, url in DATASETS.items():
        download(name, url)

    for f in DATA_DIR.glob("*.csv"):
        if "prepared" not in f.name:
            normalize_dataset(f)

if __name__ == "__main__":
    main()
