import os
import json
import pandas as pd
import requests

DATA_DIR = "real-data"
os.makedirs(DATA_DIR, exist_ok=True)


def save_dataset(name, df):
    path = os.path.join(DATA_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    print("saved", path)


def fetch_sunspots():
    url = "https://www.sidc.be/silso/DATA/SN_d_tot_V2.0.txt"
    r = requests.get(url, timeout=30)
    rows = []

    for line in r.text.splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        value = float(parts[3])
        rows.append({"t": f"{year}-{month}-{day}", "value": value})

    df = pd.DataFrame(rows)
    save_dataset("sunspots_global", df)


def fetch_bitcoin():
    url = "https://api.coindesk.com/v1/bpi/historical/close.json"
    r = requests.get(url, timeout=30)
    data = r.json()["bpi"]

    rows = [{"t": k, "value": v} for k, v in data.items()]
    df = pd.DataFrame(rows)

    save_dataset("bitcoin_price", df)


def fetch_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    r = requests.get(url, timeout=30)
    data = r.json()["features"]

    rows = []

    for f in data:
        t = f["properties"]["time"]
        mag = f["properties"]["mag"]
        if mag is None:
            continue
        rows.append({"t": t, "value": mag})

    df = pd.DataFrame(rows)

    save_dataset("earthquake_magnitude", df)


def fetch_geomagnetic():
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    r = requests.get(url, timeout=30)
    data = r.json()

    rows = []

    for d in data:
        rows.append({
            "t": d["time_tag"],
            "value": float(d["kp_index"])
        })

    df = pd.DataFrame(rows)

    save_dataset("geomagnetic_kp", df)


def main():

    try:
        fetch_sunspots()
    except Exception as e:
        print("sunspots failed", e)

    try:
        fetch_bitcoin()
    except Exception as e:
        print("bitcoin failed", e)

    try:
        fetch_earthquakes()
    except Exception as e:
        print("earthquakes failed", e)

    try:
        fetch_geomagnetic()
    except Exception as e:
        print("geomagnetic failed", e)

    print("global chaos datasets ready")


if __name__ == "__main__":
    main()
