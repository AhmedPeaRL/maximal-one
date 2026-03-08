import os
import urllib.request
import pandas as pd
import numpy as np

DATASETS = {
    "sunspots": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv"
}

OUTPUT_DIR = "real-data"


def download_dataset(name, url):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    path = os.path.join(OUTPUT_DIR, f"{name}.csv")

    if os.path.exists(path):
        print(f"{name} already exists")
        return path

    print(f"Downloading {name}...")

    urllib.request.urlretrieve(url, path)

    print(f"Saved to {path}")
    return path


def normalize_series(series):
    series = np.array(series, dtype=float)

    mean = np.mean(series)
    std = np.std(series)

    if std == 0:
        return series

    return (series - mean) / std


def prepare_dataset(name, path):

    df = pd.read_csv(path)

    col = df.columns[-1]

    series = normalize_series(df[col])

    out_path = os.path.join(OUTPUT_DIR, f"{name}_prepared.csv")

    pd.DataFrame({"value": series}).to_csv(out_path, index=False)

    print(f"Prepared dataset: {out_path}")


def main():

    for name, url in DATASETS.items():

        path = download_dataset(name, url)

        prepare_dataset(name, path)


if __name__ == "__main__":
    main()
