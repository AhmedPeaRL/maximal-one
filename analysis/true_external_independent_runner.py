"""Compatibility entry point: external artifact retrieval/hash, not replication."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from analysis.public_artifact_retrieval import fetch_text


def run() -> int:
    fetched = fetch_text()
    result = {
        "timestamp": time.time(),
        "protocol": "PUBLIC_ARTIFACT_RETRIEVAL_HASH_V1",
        "status": fetched["status"],
        "http_status": fetched["http_status"],
        "attempts": fetched["attempts"],
        "external_hash": None,
        "source": "public_github_raw_artifact_same_repository",
        "retrieval_succeeded": fetched["raw_text"] is not None,
        "verification_status": fetched["status"],
        "scientific_claim_authority": False,
        "promotion_authority": False,
        "independent_code_execution": False,
        "independent_implementation_replication": False,
        "independent_laboratory_replication": False,
        "independent_scientific_replication": False,
        "error": fetched["error"],
        "interpretation": (
            "This process attempts to retrieve and hash a public canonical artifact. It does not rerun "
            "the scientific pipeline and does not constitute independent scientific verification."
        ),
    }
    if fetched["raw_text"] is not None:
        try:
            data = json.loads(fetched["raw_text"])
            raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
            result["external_hash"] = hashlib.sha256(raw).hexdigest()
            result["status"] = "RETRIEVED_AND_HASHED_NOT_REPLICATION"
            result["verification_status"] = result["status"]
        except (TypeError, ValueError) as exc:
            result["status"] = "INVALID_JSON"
            result["verification_status"] = result["status"]
            result["error"] = f"{type(exc).__name__}: {exc}"
    Path("external_artifact_retrieval.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
