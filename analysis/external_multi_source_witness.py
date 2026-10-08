#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json

import requests


SOURCES = [
    "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/canonical_report.json",
    "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json",
    "https://cdn.jsdelivr.net/gh/ahmedpearl/maximal-one@main/public/repro_bundle/canonical_report.json",
    "https://raw.githack.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json",
]

TIMEOUT_SECONDS = 15


def inspect_source(url: str) -> dict:
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        raw = response.content

        if not raw.strip():
            return {
                "url": url,
                "status": "empty_response",
            }

        try:
            payload = json.loads(
                raw.decode("utf-8")
            )
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {
                "url": url,
                "status": "invalid_json",
            }

        if not isinstance(payload, dict):
            return {
                "url": url,
                "status": "invalid_json_shape",
            }

        return {
            "url": url,
            "status": "ok",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "_raw": raw,
        }

    except requests.Timeout:
        return {
            "url": url,
            "status": "timeout",
        }

    except requests.RequestException:
        return {
            "url": url,
            "status": "request_error",
        }


def main() -> None:
    checks = [
        inspect_source(url)
        for url in SOURCES
    ]

    successful = [
        item
        for item in checks
        if item["status"] == "ok"
    ]

    distinct_hashes = sorted({
        item["sha256"]
        for item in successful
    })

    if not successful:
        detail = "unavailable"

    elif len(distinct_hashes) > 1:
        detail = "mirror_mismatch"

    elif len(successful) >= 2:
        detail = "mirror_consistent"

    else:
        detail = "single_mirror_only"

    result = {
        "protocol": "EXTERNAL_MIRROR_CONSISTENCY_V1",
        "scientific_role": "diagnostic_only",
        "independent_scientific_replication": False,
        "status": (
            "multi_mirror_verified"
            if detail == "mirror_consistent"
            else "degraded"
        ),
        "verification_detail": detail,
        "successful_mirror_count": len(successful),
        "distinct_content_hash_count": len(distinct_hashes),
        "content_sha256": (
            distinct_hashes[0]
            if len(distinct_hashes) == 1
            else None
        ),
        "sources": [
            {
                key: value
                for key, value in item.items()
                if key != "_raw"
            }
            for item in checks
        ],
    }

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
