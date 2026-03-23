import json
from pathlib import Path

ART = Path("artifacts")


def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


def main():

    closer = load("reality_gap_closer.json")
    detector_v2 = load("reality_gap_detector_v2.json")

    if not closer:
        print(json.dumps({"passed": False, "reason": "missing_closer"}))
        return

    if closer.get("skipped", False):
        print(json.dumps({"passed": False, "reason": "skipped"}))
        return

    if not closer.get("beyond_random", False):
        print(json.dumps({"passed": False, "reason": "still_random"}))
        return

    # 🔥 NEW: detector consistency check
    if detector_v2 and detector_v2.get("gap_detected", False):
        result = {
            "passed": False,
            "reason": "detector_inconsistency"
        }
    else:
        result = {
            "passed": True,
            "reason": "signal_beyond_random_and_structured"
        }

    (ART / "reality_gap_fixed.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
