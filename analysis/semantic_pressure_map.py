import json
import os

def build_pressure_map():
    signals = {}

    if os.path.exists("artifacts/stability_status.json"):
        with open("artifacts/stability_status.json") as f:
            s = json.load(f)
        signals["stability"] = s

    if os.path.exists("artifacts/runtime_divergence.json"):
        with open("artifacts/runtime_divergence.json") as f:
            d = json.load(f)
        signals["divergence"] = d

    pressure = len(signals.get("stability", {}).get("issues", []))

    result = {
        "pressure_score": pressure,
        "state": "compressed" if pressure > 2 else "open",
        "signals": signals
    }

    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/pressure_map.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Pressure map built:", result)


if __name__ == "__main__":
    build_pressure_map()
