from __future__ import annotations

import json
from pathlib import Path
import time

STATE_PATH = Path(
    "data/adaptive_state.json"
)

REPORT_PATH = Path(
    "artifacts/canonical_report.json"
)

def load_report():
    if not REPORT_PATH.exists():
        return None

    try:
        return json.loads(
            REPORT_PATH.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return None

def load_state():
    if not STATE_PATH.exists():
        return {
            "history": [],
            "weights": {
                "alpha": 1.0,
                "sigma": 1.0,
                "confidence": 1.0,
            },
            "mode": "diagnostic_only",
        }

    return json.loads(
        STATE_PATH.read_text(
            encoding="utf-8"
        )
    )

def save_state(state):
    STATE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    STATE_PATH.write_text(
        json.dumps(
            state,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8",
    )

def extract_signal(report):
    try:
        spectral = report[
            "spectral_profile"
        ]

        return {
            "alpha": spectral[
                "estimated_alpha"
            ],
            "sigma": spectral[
                "bootstrap_std"
            ],
            "claim_status": report[
                "scientific_interpretation"
            ].get(
                "claim_status",
                "unknown"
            ),
            "claim_support_gate": report[
                "scientific_interpretation"
            ].get(
                "claim_support_gate",
                False
            ),
        }

    except Exception:
        return {}

def main():
    report = load_report()

    if report is None:
        print("No canonical report found.")
        return

    state = load_state()
    signal = extract_signal(report)

    state["history"].append(
        {
            "timestamp": time.time(),
            "signal": signal,
            "weights_changed": False,
            "mode": "diagnostic_only",
        }
    )

    state["epistemic_policy"] = {
        "adaptive_weights_affect_scientific_claim": False,
        "adaptive_state_affects_canonical_report": False,
        "market_execution_authorized": False,
    }

    save_state(state)

    print(
        "Adaptive state recorded diagnostically only."
    )

if __name__ == "__main__":
    main()
