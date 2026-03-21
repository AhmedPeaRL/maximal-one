import json
import pathlib
import hashlib

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


def main():
    verdict = load("global_verdict.json")
    universality = load("universality_stability.json")

    if not verdict or not universality:
        print(json.dumps({"status": "incomplete"}))
        return

    signal = {
        "scientific_score": verdict.get("final_score", 0),
        "confidence": verdict.get("confidence_level", "unknown"),
        "universality_stable": universality.get("passed", False)
    }

    encoded = json.dumps(signal, sort_keys=True).encode()
    fingerprint = hashlib.sha256(encoded).hexdigest()

    result = {
        "market_ready": (
            signal["scientific_score"] >= 0.65 and
            signal["universality_stable"]
        ),
        "signal": signal,
        "fingerprint": fingerprint
    }

    ART.mkdir(exist_ok=True)
    (ART / "market_signal.json").write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
