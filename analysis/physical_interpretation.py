import json
import numpy as np

def classify_alpha(alpha):
    """
    Rough physical interpretation of spectral exponent
    """

    if alpha < 0.3:
        return "white_noise"
    elif 0.3 <= alpha < 0.8:
        return "weakly_correlated"
    elif 0.8 <= alpha < 1.5:
        return "1_f_like (complex system)"
    elif 1.5 <= alpha < 2.5:
        return "brownian_like"
    else:
        return "strongly_nonstationary"


def main():
    r = json.load(open("artifacts/canonical_report.json"))

    alpha = r["spectral_profile"]["estimated_alpha"]

    interpretation = classify_alpha(alpha)

    out = {
        "alpha": alpha,
        "interpretation": interpretation
    }

    with open("artifacts/physical_interpretation.json", "w") as f:
        json.dump(out, f, indent=2)

    print("✅ Physical interpretation generated:", interpretation)


if __name__ == "__main__":
    main()
