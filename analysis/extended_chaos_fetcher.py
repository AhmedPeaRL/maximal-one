import os
import pandas as pd
import requests

DATA_DIR = "real-data"
os.makedirs(DATA_DIR, exist_ok=True)


def save_dataset(name, df):
    path = os.path.join(DATA_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    print("saved", path)


def fetch_enso():
    url = "https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.data"
    r = requests.get(url, timeout=30)

    rows = []

    for line in r.text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#") or line.startswith("<"):
            continue

        parts = line.split()

        if len(parts) < 13:
            continue

        try:
            year = int(parts[0])
        except:
            continue

        for i in range(1, 13):

            val = parts[i]

            if val == "-99.99":
                continue

            try:
                value = float(val)
            except:
                continue

            rows.append({
                "t": f"{year}-{i}",
                "value": value
            })

    df = pd.DataFrame(rows)
    save_dataset("enso_nino34", df)


def fetch_cosmic_rays():

    url = "https://www.nmdb.eu/nest/draw_graph.php?formchk=1&stations[]=OULU&tabchoice=revori&dtype=corr_for_efficiency&tresolution=60&yunits=0&date_choice=bydate&start_day=01&start_month=01&start_year=2020&start_hour=00&start_min=00&end_day=01&end_month=01&end_year=2024&end_hour=00&end_min=00&output=ascii"

    r = requests.get(url, timeout=30)

    rows = []

    for line in r.text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#") or line.startswith("<"):
            continue

        parts = line.split()

        if len(parts) < 3:
            continue

        try:
            value = float(parts[2])
        except:
            continue

        rows.append({
            "t": parts[0] + "T" + parts[1],
            "value": value
        })

    df = pd.DataFrame(rows)
    save_dataset("cosmic_rays", df)


def fetch_co2():

    url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv"

    r = requests.get(url, timeout=30)

    rows = []

    for line in r.text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        parts = line.split(",")

        if len(parts) < 4:
            continue

        year = parts[0]
        month = parts[1]

        try:
            value = float(parts[3])
        except:
            continue

        if value == -99.99:
            continue

        rows.append({
            "t": f"{year}-{month}",
            "value": value
        })

    df = pd.DataFrame(rows)
    save_dataset("co2_atmospheric", df)


def fetch_solar_wind():

    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"

    r = requests.get(url, timeout=30)

    data = r.json()

    rows = []

    for row in data[1:]:

        if row[2] is None:
            continue

        try:
            value = float(row[2])
        except:
            continue

        rows.append({
            "t": row[0],
            "value": value
        })

    df = pd.DataFrame(rows)
    save_dataset("solar_wind_speed", df)


def main():

    try:
        fetch_enso()
    except Exception as e:
        print("enso failed", e)

    try:
        fetch_cosmic_rays()
    except Exception as e:
        print("cosmic rays failed", e)

    try:
        fetch_co2()
    except Exception as e:
        print("co2 failed", e)

    try:
        fetch_solar_wind()
    except Exception as e:
        print("solar wind failed", e)

    try:
        download_dataset()
    except Exception:
        print("network failed — using local snapshot")
        load_local_copy()

    print("extended chaos datasets ready")


if __name__ == "__main__":
    main()
