import json
import sys
import os

STRICT_CLAIM_PATH = "core-scientific/strict_claim.json"
UNIFIED_CLAIM_PATH = "core-scientific/unified_claim.json"
EXTERNAL_CLASSIFICATION_PATH = "artifacts/external_classification.json"
CANONICAL_REPORT_PATH = "artifacts/canonical_report.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_alpha_source():
    """
    Determine which alpha is being validated.

    External classification is treated as an external-domain
    validation result. It is evaluated against the canonical
    scientific validity range declared in strict_claim.json.

    The legacy physical/emergent ranges in unified_claim.json
    remain diagnostic classification information and are not
    used as the canonical falsification range for external data.
    """

    if os.path.exists(EXTERNAL_CLASSIFICATION_PATH):
        result = load_json(EXTERNAL_CLASSIFICATION_PATH)

        if "alpha" not in result:
            raise ValueError(
                "external_classification.json is missing required field: alpha"
            )

        return float(result["alpha"]), None, "external"

    report = load_json(CANONICAL_REPORT_PATH)

    spectral = report.get("spectral_profile", {})

    if "estimated_alpha" not in spectral:
        raise ValueError(
            "canonical_report.json is missing spectral_profile.estimated_alpha"
        )

    alpha = float(spectral["estimated_alpha"])

    sigma = spectral.get("bootstrap_std")

    if sigma is not None:
        sigma = float(sigma)

    return alpha, sigma, "canonical"

def validate_finite(value, name):
    if not isinstance(value, (int, float)) or not float("-inf") < value < float("inf"):
        print(f"❌ Non-finite {name}: {value}")
        sys.exit(1)

def main():
    alpha, sigma, source = load_alpha_source()
    
    validate_finite(alpha, "alpha")

    strict_claim = load_json(STRICT_CLAIM_PATH)

    expected = strict_claim.get("expected_result", {})
    strict_range = expected.get("alpha_range")

    if (
        not isinstance(strict_range, list)
        or len(strict_range) != 2
        or not all(isinstance(x, (int, float)) for x in strict_range)
    ):
        print(
            "❌ Missing or invalid "
            "strict_claim expected_result.alpha_range"
        )
        sys.exit(1)

    strict_min, strict_max = map(float, strict_range)

    # ------------------------------------------------------------------
    # Canonical scientific validity range
    # ------------------------------------------------------------------
    #
    # This is the machine-gated scientific validity range declared by
    # strict_claim.json.
    #
    # It is distinct from the legacy physical/emergent classification
    # ranges in unified_claim.json.
    #
    # External-domain results are evaluated against this canonical range.
    # ------------------------------------------------------------------

    if not (strict_min <= alpha <= strict_max):
        print(
            f"❌ Alpha خارج النطاق العلمي canonical: "
            f"{alpha} not in [{strict_min}, {strict_max}]"
        )
        sys.exit(1)

    # ------------------------------------------------------------------
    # Optional legacy classification information
    # ------------------------------------------------------------------
    #
    # unified_claim.json may contain physical/emergent ranges.
    # These ranges are retained as diagnostic classification metadata.
    # They are not the canonical falsification range for external-domain
    # validation.
    # ------------------------------------------------------------------

    unified_claim = load_json(UNIFIED_CLAIM_PATH)

    adaptive = unified_claim.get("adaptive_alpha", {})
    legacy_range = adaptive.get("alpha_range")

    if source == "external":
        if (
            isinstance(legacy_range, list)
            and len(legacy_range) == 2
            and all(isinstance(x, (int, float)) for x in legacy_range)
        ):
            legacy_min, legacy_max = map(float, legacy_range)

            if not (legacy_min <= alpha <= legacy_max):
                print(
                    "ℹ️ External alpha is outside the legacy unified "
                    f"classification range [{legacy_min}, {legacy_max}]."
                )
                print(
                    "ℹ️ This is diagnostic classification information only; "
                    "canonical scientific validity is governed by "
                    "strict_claim.json."
                )

    # ------------------------------------------------------------------
    # Sigma validation
    # ------------------------------------------------------------------

    adaptive_sigma = unified_claim.get("adaptive_sigma", {})

    max_sigma = adaptive_sigma.get("max_sigma")

    if max_sigma is not None:
        max_sigma = float(max_sigma)

    multiplier = adaptive_sigma.get("max_sigma_multiplier", 2.5)
    multiplier = float(multiplier)

    if max_sigma is not None and sigma is not None:
        allowed_sigma = max_sigma * multiplier

        if sigma > allowed_sigma:
            print(
                f"❌ Sigma عالي: {sigma} "
                f"(allowed diagnostic limit: {allowed_sigma})"
            )
            sys.exit(1)

    # ------------------------------------------------------------------
    # Final status
    # ------------------------------------------------------------------

    if source == "external":
        print(
            f"✅ External alpha scientifically valid: "
            f"{alpha} within canonical range "
            f"[{strict_min}, {strict_max}]"
        )
        print(
            "ℹ️ External-domain alpha is not required to satisfy "
            "legacy physical/emergent classification ranges."
        )
    else:
        print(
            f"✅ Canonical alpha scientifically valid: "
            f"{alpha} within [{strict_min}, {strict_max}]"
        )

    print("✅ Alpha physical/canonical guard passed")

if __name__ == "__main__":
    main()
