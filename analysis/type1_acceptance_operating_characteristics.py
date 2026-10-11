#!/usr/bin/env python3
"""Reproduce operating characteristics of the current Type-I gate.

Standard-library only. This is an audit utility; it does not alter or run the
production scientific gate and does not approve or freeze any null protocol.
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Iterable

WILSON_Z_95 = 1.959963984540054


def wilson_interval(x: int, n: int, z: float = WILSON_Z_95) -> tuple[float, float]:
    """Return the two-sided Wilson score interval for a binomial proportion."""
    if n <= 0 or not 0 <= x <= n:
        raise ValueError("Require n > 0 and 0 <= x <= n")
    p_hat = x / n
    z2 = z * z
    denominator = 1.0 + z2 / n
    center = (p_hat + z2 / (2.0 * n)) / denominator
    radius = (z / denominator) * math.sqrt(
        p_hat * (1.0 - p_hat) / n + z2 / (4.0 * n * n)
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def binomial_probabilities(n: int, p: float) -> list[float]:
    """Return normalized Binomial(n,p) probabilities using log probabilities."""
    if n < 0 or not 0.0 <= p <= 1.0:
        raise ValueError("Require n >= 0 and 0 <= p <= 1")
    if p == 0.0:
        return [1.0] + [0.0] * n
    if p == 1.0:
        return [0.0] * n + [1.0]
    log_p, log_q = math.log(p), math.log1p(-p)
    logs = [
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        + k * log_p + (n - k) * log_q
        for k in range(n + 1)
    ]
    maximum = max(logs)
    weights = [math.exp(value - maximum) for value in logs]
    total = sum(weights)
    return [weight / total for weight in weights]


def accepted_counts(
    n: int,
    nominal_p: float,
    upper_limit: float,
    z: float = WILSON_Z_95,
) -> list[int]:
    """Counts accepted by the production rule: CI contains nominal_p and upper <= limit."""
    if n <= 0 or not 0.0 < nominal_p < 1.0 or not 0.0 < upper_limit < 1.0:
        raise ValueError("Require n > 0 and both probabilities strictly between 0 and 1")
    accepted = []
    for x in range(n + 1):
        lower, upper = wilson_interval(x, n, z)
        if lower <= nominal_p <= upper and upper <= upper_limit:
            accepted.append(x)
    return accepted


def summarize(n: int = 1000, nominal_p: float = 0.05,
              upper_limit: float = 0.075, scenarios: int = 4) -> dict:
    """Compute operating characteristics of the production rule under iid Binomial assumptions."""
    if scenarios < 1:
        raise ValueError("scenarios must be >= 1")
    accepted = accepted_counts(n, nominal_p, upper_limit)
    probs = binomial_probabilities(n, nominal_p)
    pass_probability = sum(probs[x] for x in accepted)
    result = {
        "protocol": "TYPE1_ACCEPTANCE_RULE_OPERATING_CHARACTERISTICS_AUDIT_V1",
        "audit_only": True,
        "production_gate_modified": False,
        "assumption": "independent Bernoulli repetitions with common rejection probability",
        "n": n,
        "nominal_p": nominal_p,
        "wilson_two_sided_confidence": 0.95,
        "wilson_upper_limit": upper_limit,
        "accepted_rejection_count_min": min(accepted),
        "accepted_rejection_count_max": max(accepted),
        "accepted_rejection_count_rule": "two-sided Wilson 95% interval must contain nominal_p AND Wilson upper endpoint <= upper_limit",
        "wilson_lower_at_previous_count": wilson_interval(min(accepted) - 1, n)[0] if min(accepted) > 0 else None,
        "wilson_upper_at_previous_count": wilson_interval(min(accepted) - 1, n)[1] if min(accepted) > 0 else None,
        "wilson_lower_at_min_accepted": wilson_interval(min(accepted), n)[0],
        "wilson_upper_at_min_accepted": wilson_interval(min(accepted), n)[1],
        "wilson_upper_at_max_accepted": wilson_interval(max(accepted), n)[1],
        "wilson_upper_at_next_count": wilson_interval(max(accepted) + 1, n)[1]
        if max(accepted) < n else None,
        "pass_probability_one_nominal_scenario": pass_probability,
        "false_fail_probability_one_nominal_scenario": 1.0 - pass_probability,
        "pass_probability_all_scenarios_if_independent": pass_probability ** scenarios,
        "probability_at_least_one_false_fail_if_scenarios_independent": 1.0 - pass_probability ** scenarios,
        "scenarios_assumed_independent_for_family_calculation": scenarios,
        "exact_binomial_upper_tail_examples": {
            str(x): sum(probs[x:]) for x in (60, 73) if x <= n
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--nominal-p", type=float, default=0.05)
    parser.add_argument("--upper-limit", type=float, default=0.075)
    parser.add_argument("--scenarios", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(summarize(args.n, args.nominal_p, args.upper_limit, args.scenarios), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
