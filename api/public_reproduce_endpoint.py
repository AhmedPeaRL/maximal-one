"""Retired helper: this file is not an HTTP route or a safe reproduction service.

The previous implementation cloned a mutable default branch, installed dependencies
at request time, had no execution timeout/resource isolation, and invoked a script
that did not consume the supplied payload or produce the expected result file.

This module intentionally fails closed. It performs no network, subprocess,
filesystem, or scientific-analysis operation.
"""

from __future__ import annotations


def run_external_reproduction(input_payload: dict) -> dict:
    """Preserve the old import surface while refusing unsafe execution."""
    raise RuntimeError(
        "PUBLIC_REPRODUCTION_HELPER_RETIRED: this module is not an HTTP endpoint "
        "and is not authorized to execute repository code. Use the reviewed "
        "clean-checkout computational reproducibility protocol instead."
    )


if __name__ == "__main__":
    raise SystemExit(
        "DISABLED: this module is not a public HTTP route or executable service."
    )
