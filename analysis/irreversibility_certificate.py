import json
from pathlib import Path
from datetime import datetime
import hashlib

ART = Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

def sha256_of_file(path):
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()

def main():
    irr = load("irreversibility_enforced.json")
    verdict = load("global_verdict.json")
    uni = load("universality_stability.json")

    if not irr or not irr.get("irreversible"):
        print("System not irreversible — no certificate issued")
        return

    certificate = {
        "certificate": "HCM_IRREVERSIBILITY_PROOF",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "confirmed",
        "confidence": "empirical-high" if irr.get("confidence") == "high" else "bounded",
        "score": irr.get("irreversibility_score"),

        "scientific_basis": {
            "predictive_score": verdict.get("score_ratio"),
            "final_score": verdict.get("final_score"),
            "universality_runs": uni.get("progress", {}).get("runs"),
            "stability_score": uni.get("score")
        },

        "integrity": {
            "verdict_hash": sha256_of_file("artifacts/global_verdict.json"),
            "irreversibility_hash": sha256_of_file("artifacts/irreversibility_enforced.json"),
            "universality_hash": sha256_of_file("artifacts/universality_stability.json")
        }
    }

    (ART / "irreversibility_certificate.json").write_text(
        json.dumps(certificate, indent=2)
    )

    print(json.dumps(certificate, indent=2))

if __name__ == "__main__":
    main()
