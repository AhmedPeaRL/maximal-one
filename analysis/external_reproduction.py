import requests
import json

URL = "https://ahmedpearl.github.io/maximal-one/public/irreducible_truth.json"

def run():
    print("Fetching external truth...")

    r = requests.get(URL, timeout=10)
    data = r.json()

    alpha = data["core_claim"]["measured_alpha"]
    sigma = data["core_claim"]["uncertainty_sigma"]

    print("Alpha:", alpha)
    print("Sigma:", sigma)

    if 0.45 <= alpha <= 0.60 and sigma <= 0.05:
        print("✅ External validation PASSED")
    else:
        print("❌ External validation FAILED")

if __name__ == "__main__":
    run()
