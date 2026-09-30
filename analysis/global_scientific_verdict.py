from __future__ import annotations

import json
from pathlib import Path

ART = Path("artifacts")
OUTPUT = ART / "global_verdict.json"

def load(name):
    path = ART / name

    if not path.exists():
        return None

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return None

canonical = load(
    "canonical_report.json"
)

contract = load(
    "scientific_contract_evaluation.json"
)

claim = load(
    "claim_readiness_audit.json"
)

result = {
    "status": "DIAGNOSTIC_ONLY",
    "scientific_claim_authority": False,
    "promotion_authority": False,

    "scientific_decision": {
        "claim_supported": False,
        "promotion_allowed": False,
        "decision_source":
            "authoritative_scientific_contract_only",
    },

    "diagnostic_sources": {
        "canonical_report_present":
            canonical is not None,

        "scientific_contract_present":
            contract is not None,

        "claim_readiness_audit_present":
            claim is not None,
    },

    "forbidden_operations": [
        "deterministic_noise",
        "heuristic_evidence_bonuses",
        "weighted_score_as_scientific_evidence",
        "frontier_classification",
        "market_authorization",
        "causal_inference",
        "universality_inference",
    ],

    "interpretation": (
        "This artifact is a non-authoritative diagnostic "
        "summary only. Scientific claim support and promotion "
        "must be determined exclusively by the machine-gated "
        "scientific contract and strict promotion gate. "
        "No score, bonus, deterministic noise, layer label, "
        "or heuristic aggregation may create scientific evidence."
    ),
}

ART.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)

print(
    json.dumps(
        result,
        indent=2,
    )
)
