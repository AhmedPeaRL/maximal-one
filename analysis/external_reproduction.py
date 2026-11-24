"""Retired static-report fetcher; not an independent reproduction mechanism.

The former implementation fetched a fixed public JSON report and compared two
thresholds. It did not rerun the scientific pipeline, consume a reproduction
payload, or establish independent replication.

A successful retrieval/hash must never be described as reproduction.
"""

from __future__ import annotations

import json
import sys


def main() -> int:
    result = {
        "schema": "HCM_RETIRED_EXTERNAL_REPRODUCTION_HELPER_V1",
        "status": "DISABLED_NOT_A_REPRODUCTION",
        "independent_code_execution": False,
        "independent_implementation_replication": False,
        "independent_laboratory_replication": False,
        "scientific_claim_authority": False,
        "promotion_authority": False,
        "reason": (
            "This legacy helper only retrieved a fixed report; it did not "
            "execute the analysis from supplied inputs."
        ),
        "next_valid_scope": (
            "clean-checkout computational reproducibility, explicitly "
            "distinguished from independent scientific replication"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
