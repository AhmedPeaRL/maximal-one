import json
import hashlib
import requests
import numpy as np

DATA_SOURCES = [
    "https://raw.githubusercontent.com/datasets/s-and-p-500/master/data/data.csv",
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv"
]

OUTPUT_PATH = "artifacts/reality_pressure.json"


def fetch_data(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        return None
    return None


def extract_signal(raw_text):
    lines = raw_text.split("\n")[1:]
    values = []

    for l in lines:
        parts = l.split(",")
        try:
            values.append(float(parts[-1]))
        except:
            continue

    if len(values) < 50:
        return None

    return np.array(values)


def analyze_signal(arr):
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    trend = float(arr[-1] - arr[0])

    return {
        "mean": mean,
        "std": std,
        "trend": trend
    }


def run():
    results = []

    for src in DATA_SOURCES:
        raw = fetch_data(src)

        if not raw:
            continue

        signal = extract_signal(raw)

        if signal is None:
            continue

        analysis = analyze_signal(signal)

        results.append({
            "source": src,
            "analysis": analysis
        })

    if not results:
        raise Exception("No valid external signals")

    payload = json.dumps(results, sort_keys=True)
    fingerprint = hashlib.sha256(payload.encode()).hexdigest()

    final = {
        "results": results,
        "fingerprint": fingerprint
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(final, f, indent=2)

    print("Reality pressure applied.")
    print("Fingerprint:", fingerprint)


if __name__ == "__main__":
    run()
