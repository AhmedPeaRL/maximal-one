import requests
import json

URL = "https://ahmedpearl.github.io/maximal-one/public/irreducible_truth.json"

def run():
    print("Fetching external truth...")

    try:
        r = requests.get(URL, timeout=10)

        print("Status Code:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type"))

        if r.status_code != 200:
            raise Exception("Non-200 response")

        if "application/json" not in r.headers.get("Content-Type", ""):
            raise Exception("Response is not JSON")

        if not r.text.strip():
            raise Exception("Empty response body")

        data = r.json()

    except Exception as e:
        print("❌ External fetch failed:", str(e))
        print("Raw response preview:")
        print(r.text[:300] if 'r' in locals() else "No response")
        return

    try:
        alpha = data["core_claim"]["measured_alpha"]
        sigma = data["core_claim"]["uncertainty_sigma"]

        print("Alpha:", alpha)
        print("Sigma:", sigma)

        if 0.45 <= alpha <= 0.60 and sigma <= 0.05:
            print("✅ External validation PASSED")
        else:
            print("❌ External validation FAILED")

    except KeyError:
        print("❌ JSON structure invalid")
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    run()
