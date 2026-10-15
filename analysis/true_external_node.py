"""Compatibility entry point: public artifact retrieval/hash diagnostic only."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from analysis.public_artifact_retrieval import fetch_text

VOLATILE_KEYS = {
    "timestamp", "_environment", "generated_at", "runtime",
    "execution_time", "host", "_sealed",
}


def normalize(raw: str) -> str | None:
    try:
        data = json.loads(raw)

        def strip(obj):
            if isinstance(obj, dict):
                return {k: strip(v) for k, v in obj.items() if k not in VOLATILE_KEYS}
            if isinstance(obj, list):
                return [strip(x) for x in obj]
            if isinstance(obj, float):
                return round(obj, 8)
            return obj

        return json.dumps(strip(data), sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError):
        return None


def main() -> int:
    fetched = fetch_text()
    result = {
        "timestamp": time.time(),
        "protocol": "PUBLIC_ARTIFACT_RETRIEVAL_HASH_V1",
        "status": fetched["status"],
        "http_status": fetched["http_status"],
        "attempts": fetched["attempts"],
        "source": "public_github_raw_artifact_same_repository",
        "external_hash": None,
        "normalization_applied": False,
        "scientific_claim_authority": False,
        "promotion_authority": False,
        "independent_code_execution": False,
        "independent_implementation_replication": False,
        "independent_scientific_replication": False,
        "error": fetched["error"],
        "interpretation": (
            "This check retrieves and hashes a public artifact only. It does not rerun the scientific pipeline "
            "and is not independent scientific replication."
        ),
    }
    if fetched["raw_text"] is not None:
        normalized = normalize(fetched["raw_text"])
        if normalized is None:
            result["status"] = "INVALID_JSON_OR_NORMALIZATION_FAILED"
            result["error"] = "The retrieved response could not be parsed as JSON."
        else:
            result["external_hash"] = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            result["normalization_applied"] = True
    Path("external_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    # Expected unavailability is diagnostic data, not a scientific-pipeline pass/fail.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
