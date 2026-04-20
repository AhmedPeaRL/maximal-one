import json
import os

INPUT_PATH = "artifacts/self_healing.json"
CONFIG_PATH = "analysis/runtime_config.json"

def main():
    if not os.path.exists(INPUT_PATH):
        print("No healing signal")
        return

    with open(INPUT_PATH) as f:
        data = json.load(f)

    action = data.get("healing_signal", {}).get("action")

    config = {}

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            config = json.load(f)

    if action == "increase_sample_size_or_filter_noise":
        config["noise_filter"] = True
        config["min_samples"] = config.get("min_samples", 1000) + 500

    elif action == "re-evaluate spectral window or scaling":
        config["spectral_window"] = "adaptive"

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print("Healing executed:", action)

if __name__ == "__main__":
    main()
