import urllib.request
from pathlib import Path

DATASETS = {
    "sunspots":
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv"
}

def download():

    Path("real-data").mkdir(exist_ok=True)

    for name, url in DATASETS.items():

        print("Downloading", name)

        path = f"real-data/{name}.csv"

        urllib.request.urlretrieve(url, path)

        print("Saved", path)


if __name__ == "__main__":
    download()
