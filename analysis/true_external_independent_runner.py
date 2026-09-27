from __future__ import annotations

import hashlib
import json
import time
import requests

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "ahmedpearl/maximal-one/main/"
    "artifacts/canonical_report.json"
)

def fetch_external():
    for attempt in range(6):
        try:
            url = (
                f"{BASE_URL}"
                f"?t={int(time.time())}"
            )

            response = requests.get(
                url,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()

            print(
                "HTTP status:",
                response.status_code,
            )

        except Exception as exc:
            print(
                "Fetch error:",
                repr(exc),
            )

        time.sleep(5)

    raise RuntimeError(
        "Failed to fetch external canonical report"
    )

def independent_hash(data):
    raw = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(
        raw
    ).hexdigest()

def run():
    data = fetch_external()

    digest = independent_hash(
        data
    )

    result = {
        "timestamp": time.time(),

        "external_hash": digest,

        "source":
            "public_github_raw_artifact",

        "retrieval_succeeded":
            True,

        "verification_status":
            "artifact_retrieved_and_independently_hashed",

        "scientific_claim_authority":
            False,

        "independent_code_execution":
            False,

        "independent_implementation_replication":
            False,

        "independent_laboratory_replication":
            False,

        "independent_scientific_replication":
            False,

        "interpretation":
            (
                "This process independently retrieves and hashes "
                "a public canonical artifact. It does not rerun "
                "the scientific pipeline and does not constitute "
                "independent scientific verification."
            ),
    }

    with open(
        "external_artifact_retrieval.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
            sort_keys=True,
        )

    print(
        "External artifact retrieval complete."
    )

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )

if __name__ == "__main__":
    run()
