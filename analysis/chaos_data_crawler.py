import urllib.request
import pandas as pd
from pathlib import Path


DATASETS = {
    "sunspots":
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv"
}


def download():

    Path("real-data").mkdir(exist_ok=True)

    for name, url in DATASETS.items():

        print("Downloading", name)

        r = requests.get(url)

        path = f"real-data/{name}.csv"

        with open(path, "wb") as f:
            f.write(r.content)

        print("Saved", path)


if __name__ == "__main__":
    download()
