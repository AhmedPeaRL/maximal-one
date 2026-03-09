# analysis/autonomous_chaos_harvester.py

import os
import requests
import pandas as pd

DATA_DIR = "real-data"

DATA_SOURCES = {

    "sunspots": "https://services.swpc.noaa.gov/json/solar-cycle/sunspots.json",

    "geomagnetic_kp": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json",

    "solar_flux": "https://services.swpc.noaa.gov/json/f10cm_flux.json"
}


def ensure_dir():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def fetch_json(url):

    r = requests.get(url, timeout=30)

    r.raise_for_status()

    return r.json()


def normalize_sunspots(data):

    rows = []

    for row in data:
        if "ssn" in row:
            rows.append(row["ssn"])

    return pd.DataFrame({"value": rows})


def normalize_kp(data):

    rows = []

    for row in data[1:]:
        try:
            rows.append(float(row[1]))
        except:
            continue

    return pd.DataFrame({"value": rows})


def normalize_flux(data):

    rows = []

    for row in data:
        if "flux" in row:
            rows.append(float(row["flux"]))

    return pd.DataFrame({"value": rows})


def save_dataset(name, df):

    path = os.path.join(DATA_DIR, f"{name}.csv")

    df.to_csv(path, index=False)

    print("saved:", path, "rows:", len(df))


def run():

    ensure_dir()

    try:

        sun = fetch_json(DATA_SOURCES["sunspots"])
        df = normalize_sunspots(sun)
        save_dataset("sunspots_live", df)

    except Exception as e:
        print("sunspots fetch failed", e)

    try:

        kp = fetch_json(DATA_SOURCES["geomagnetic_kp"])
        df = normalize_kp(kp)
        save_dataset("geomagnetic_kp", df)

    except Exception as e:
        print("kp fetch failed", e)

    try:

        flux = fetch_json(DATA_SOURCES["solar_flux"])
        df = normalize_flux(flux)
        save_dataset("solar_flux", df)

    except Exception as e:
        print("flux fetch failed", e)


if __name__ == "__main__":
    run()
