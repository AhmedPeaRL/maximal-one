import os
import requests
import pandas as pd
from pathlib import Path

DATA_DIR = Path("real-data")
DATA_DIR.mkdir(exist_ok=True)

DATASETS = [
    {
        "name":"sunspots_extended",
        "url":"https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-sunspots.csv"
    },
    {
        "name":"air_passengers",
        "url":"https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
    },
    {
        "name":"daily_female_births",
        "url":"https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-total-female-births.csv"
    }
]

def download_dataset(ds):

    path = DATA_DIR / f"{ds['name']}.csv"

    if path.exists():
        print("dataset already present:", ds["name"])
        return

    try:

        r = requests.get(ds["url"], timeout=20)

        if r.status_code != 200:
            print("failed download", ds["name"])
            return

        with open(path,"wb") as f:
            f.write(r.content)

        print("downloaded", ds["name"])

    except Exception as e:
        print("error", ds["name"], str(e))


def validate_dataset(path):

    try:

        df = pd.read_csv(path)

        numeric = df.select_dtypes(include="number")

        if numeric.shape[1] == 0:
            print("no numeric data", path.name)
            path.unlink()
            return

        if len(df) < 200:
            print("dataset too small", path.name)
            path.unlink()
            return

        print("validated", path.name)

    except Exception:
        print("invalid csv", path.name)
        path.unlink()


def main():

    for ds in DATASETS:
        download_dataset(ds)

    for f in DATA_DIR.glob("*.csv"):
        validate_dataset(f)

    print("autonomous dataset hunter finished")


if __name__ == "__main__":
    main()
