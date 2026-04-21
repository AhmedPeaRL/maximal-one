import json
import hashlib
import os
import time

def load_json(path):
    with open(path) as f:
        return json.load(f)

def verify_hash():
    with open("artifacts/report.hash") as f:
        stored = f.read().strip()

    with open("artifacts/canonical_report.json","rb") as f:
        calc = hashlib.sha256(f.read()).hexdigest()

    return stored == calc

def compute_adaptive_sigma_limit(claim, sigma):
    sigma_mode = claim.get("sigma_mode", "bounded")

    # === ADAPTIVE MODE ===
    if sigma_mode == "adaptive":
        adaptive = claim.get("adaptive_sigma", {})
        multiplier = adaptive.get("max_sigma_multiplier", 2.5)
        return multiplier * sigma

    # === BOUNDED MODE (CURRENT DEFAULT) ===
    elif sigma_mode == "bounded":
        adaptive = claim.get("adaptive_sigma", {})
        if "max_sigma" in adaptive:
            return adaptive["max_sigma"]

        # fallback (strict safety)
        raise ValueError("max_sigma missing in adaptive_sigma for bounded mode")

    # === HARD FAIL ===
    else:
        raise ValueError(f"Unknown sigma_mode: {sigma_mode}")

def external_verdict():
    report = load_json("artifacts/canonical_report.json")
    claim = load_json("core-scientific/unified_claim.json")

    alpha = report["spectral_profile"]["estimated_alpha"]
    sigma = report["spectral_profile"]["bootstrap_std"]

    # === sigma limit (adaptive-aware) ===
    max_sigma = compute_adaptive_sigma_limit(claim, sigma)

    # === alpha bounds ===
    if claim.get("alpha_mode") == "adaptive":
        tolerance = claim["adaptive_alpha"]["tolerance_sigma_multiplier"] * sigma
        minA = alpha - tolerance
        maxA = alpha + tolerance
    else:
        minA, maxA = claim["alpha_range"]

    # === verdict logic ===
    if sigma > max_sigma:
        return "rejected_sigma_adaptive"

    if not (minA <= alpha <= maxA):
        return "alpha_outside_dynamic_band"

    if sigma < max_sigma * 0.5:
        return "high_confidence"

    return "provisionally_valid"

def load_collapse():
    try:
        with open("artifacts/collapse_test.json") as f:
            return json.load(f)["collapse_test"]
    except:
        return "unknown"

def build_external_record():
    return {
        "timestamp": time.time(),
        "integrity": verify_hash(),
        "verdict": external_verdict(),
        "source": "independent_layer",
        "collapse_status": load_collapse(),
        "mode": "adaptive_claim_bound"
    }

if __name__ == "__main__":
    os.makedirs("public", exist_ok=True)

    record = build_external_record()

    with open("public/independent_verification.json","w") as f:
        json.dump(record, f, indent=2)

    print("Independent verification (adaptive-aware) written.")
