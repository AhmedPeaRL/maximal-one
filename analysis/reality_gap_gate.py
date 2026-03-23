import json
from pathlib import Path

ART = Path("artifacts")


def main():

    p = ART / "reality_gap_closer.json"

    if not p.exists():
        print(json.dumps({"passed": False, "reason": "missing"}))
        return

    d = json.loads(p.read_text())

    if d.get("skipped", False):
        print(json.dumps({"passed": False, "reason": "skipped"}))
        return

    if d.get("beyond_random", False):
        result = {"passed": True, "reason": "signal_beyond_random"}
    else:
        result = {"passed": False, "reason": "still_random_like"}

    (ART / "reality_gap_fixed.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
