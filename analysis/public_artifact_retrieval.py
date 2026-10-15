"""Fetch the public canonical artifact as a retrieval diagnostic only.

A successful fetch/hash is not independent code execution or scientific replication.
"""
from __future__ import annotations

import time
from typing import Callable, Any
import requests

URL = (
    "https://raw.githubusercontent.com/ahmedpearl/maximal-one/"
    "main/artifacts/canonical_report.json"
)


def fetch_text(
    get: Callable[..., Any] = requests.get,
    sleep: Callable[[float], None] = time.sleep,
    attempts: int = 3,
    timeout: int = 10,
) -> dict:
    """Return an explicit status instead of crashing on an unpublished 404."""
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            response = get(URL + f"?retrieval_attempt={attempt}&ts={time.time_ns()}", timeout=timeout)
            if response.status_code == 200:
                return {
                    "status": "RETRIEVED",
                    "http_status": 200,
                    "raw_text": response.text,
                    "attempts": attempt,
                    "error": None,
                }
            if response.status_code == 404:
                return {
                    "status": "UNAVAILABLE_NOT_PUBLISHED",
                    "http_status": 404,
                    "raw_text": None,
                    "attempts": attempt,
                    "error": "The public canonical_report.json path returned HTTP 404.",
                }
            last_error = f"HTTP_{response.status_code}"
        except Exception as exc:  # network failure is recorded, not mislabeled as replication
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt < attempts:
            sleep(2)
    return {
        "status": "UNAVAILABLE_FETCH_ERROR",
        "http_status": None,
        "raw_text": None,
        "attempts": attempts,
        "error": last_error or "Unknown retrieval error",
    }
