import json
import os
import time

OUTPUT_PATH = "data/market_signal.json"

def load_signal():
    try:
        with open(
            "artifacts/canonical_report.json",
            encoding="utf-8",
        ) as f:
            report = json.load(f)

        return {
            "alpha": report["spectral_profile"]["estimated_alpha"],
            "sigma": report["spectral_profile"]["bootstrap_std"],
        }

    except Exception:
        return None

def decide(signal):
    if signal is None:
        return {
            "action": "observe",
            "reason": "scientific_signal_unavailable",
        }

    return {
        "action": "observe",
        "reason": (
            "Market execution is disabled. "
            "Scientific spectral output is not a "
            "trading authorization."
        ),
    }

def main():
    signal = load_signal()

    decision = decide(signal)

    payload = {
        "timestamp": time.time(),
        "signal": signal,
        "decision": decision,
        "epistemic_policy": {
            "market_execution_enabled": False,
            "trading_authorization": False,
            "scientific_output_authorizes_financial_action": False,
        },
    }

    os.makedirs(
        "data",
        exist_ok=True,
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            payload,
            f,
            indent=2,
        )

    print(
        "Market bridge remains observation-only:",
        decision,
    )

if __name__ == "__main__":
    main()
