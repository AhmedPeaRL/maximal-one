import json
import os

REPORT_PATH = "artifacts/canonical_report.json"
COLLAPSE_PATH = "artifacts/collapse_test.json"
OUTPUT_PATH = "artifacts/self_healing.json"


def load(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def analyze_failure(collapse):
    if not collapse:
        return {"status": "no_data"}

    verdict = collapse.get("collapse_test")

    if verdict == "collapse_sigma_dominant_noise":
        return {
            "issue": "noise dominance",
            "action": "increase_sample_size_or_filter_noise"
        }

    if verdict == "collapse_alpha_vanish":
        return {
            "issue": "alpha instability",
            "action": "re-evaluate spectral window or scaling"
        }

    return {
        "issue": "none",
        "action": "maintain_current_state"
    }


def run():
    report = load(REPORT_PATH)
    collapse = load(COLLAPSE_PATH)

    healing = analyze_failure(collapse)

    result = {
        "healing_signal": healing,
        "status": "adaptive_response_generated"
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("Self-healing response generated")


if __name__ == "__main__":
    run()
