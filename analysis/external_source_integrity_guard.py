import os
import re
from urllib.parse import urlparse

import requests


def main():
    url = os.getenv("EXTERNAL_SOURCE_URL", "").strip()

    if not url:
        raise SystemExit("FAIL: EXTERNAL_SOURCE_URL is missing")

    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise SystemExit("FAIL: external source must use HTTPS")

    if parsed.hostname != "raw.githubusercontent.com":
        raise SystemExit("FAIL: unexpected external source host")

    expected_path = (
        "/ahmedpearl/maximal-one/main/artifacts/fingerprint.txt"
    )

    if parsed.path != expected_path or parsed.query or parsed.fragment:
        raise SystemExit("FAIL: unexpected fingerprint source path")

    try:
        response = requests.get(
            url,
            timeout=(5, 10),
            allow_redirects=False,
            headers={"Cache-Control": "no-cache"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise SystemExit(
            f"FAIL: public fingerprint fetch failed: {exc}"
        ) from exc

    fingerprint = response.text.strip()

    if not re.fullmatch(r"[0-9a-fA-F]{64}", fingerprint):
        raise SystemExit(
            "FAIL: fetched content is not a 64-character SHA-256 fingerprint"
        )

    print("Public fingerprint fetch: PASS")
    print("Fingerprint format: PASS")
    print(
        "LIMITATION: this check does not establish source integrity "
        "or independent scientific reproduction."
    )


if __name__ == "__main__":
    main()
