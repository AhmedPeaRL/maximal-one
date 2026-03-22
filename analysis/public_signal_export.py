import json
from pathlib import Path

ART = Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

def main():
    irr = load("irreversibility_enforced.json")
    verdict = load("global_verdict.json")

    public = {
        "claim": "HCM demonstrates persistent cross-system predictive structure",
        "status": "verified" if irr and irr.get("irreversible") else "unverified",
        "confidence": irr.get("confidence") if irr else "unknown",
        "evidence_strength": verdict.get("confidence_level") if verdict else "unknown"
    }

    (ART / "public_signal.json").write_text(
        json.dumps(public, indent=2)
    )

    print(json.dumps(public, indent=2))

if __name__ == "__main__":
    main()
