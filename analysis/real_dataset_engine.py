import pandas as pd
import numpy as np
import os
import requests

DATASETS = {
    "sunspots": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv",
}

OUTPUT_DIR = "real-data"

def download_dataset(name, url):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.csv")

    if os.path.exists(path):
        print(f"{name} already exists")
        return path

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    with open(path, "wb") as f:
        f.write(r.content)

    print(f"Downloaded {name}")
    return path


def normalize_series(series):
    series = np.array(series, dtype=float)
    series = (series - np.mean(series)) / np.std(series)
    return series


def prepare_dataset(name, path):
    df = pd.read_csv(path)

    col = df.columns[-1]
    series = normalize_series(df[col])

    out = os.path.join(OUTPUT_DIR, f"{name}_prepared.csv")

    pd.DataFrame({"value": series}).to_csv(out, index=False)

    print(f"Prepared dataset: {out}")


def main():

    for name, url in DATASETS.items():
        path = download_dataset(name, url)
        prepare_dataset(name, path)


if __name__ == "__main__":
    main()
