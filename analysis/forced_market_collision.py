from __future__ import annotations

import json
from pathlib import Path

REPORT_PATH = Path("artifacts/canonical_report.json")
OUTPUT_FILE = Path("public/market_collision_signal.json")

def load_signal():
    if not REPORT_PATH.exists():
        return None

    try:
        with REPORT_PATH.open("r", encoding="utf-8") as f:
            report = json.load(f)

        spectral = report.get("spectral_profile", {})
        interpretation = report.get(
            "scientific_interpretation",
            {}
        )

        return {
            "alpha": spectral.get("estimated_alpha"),
            "sigma": spectral.get("bootstrap_std"),
            "claim_status": interpretation.get(
                "claim_status",
                "unknown"
            ),
            "claim_support_gate": interpretation.get(
                "claim_support_gate",
                False
            ),
        }

    except Exception:
        return None

def build_market_signal(signal):
    if not signal:
        return {
            "status": "no_signal",
            "action": "observe",
            "scientific_authority": False,
        }

    return {
        "status": "diagnostic_only",
        "action": "observe",
        "scientific_authority": False,
        "trading_authorization": False,
        "reason": (
            "The canonical scientific report is diagnostic only. "
            "No market confidence, trading signal, or execution "
            "authorization is inferred from alpha or bootstrap sigma."
        ),
        "source_claim_status": signal["claim_status"],
        "source_claim_support_gate": signal[
            "claim_support_gate"
        ],
    }

def main():
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    signal = load_signal()
    decision = build_market_signal(signal)

    payload = {
        "decision": decision,
        "signal": signal,
        "epistemic_policy": {
            "scientific_report_authorizes_trading": False,
            "bootstrap_sigma_authorizes_trading": False,
            "alpha_authorizes_trading": False,
            "external_market_execution_enabled": False,
        },
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            payload,
            indent=2
        )
    )

if __name__ == "__main__":
    main()
