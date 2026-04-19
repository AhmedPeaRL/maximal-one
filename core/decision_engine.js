export function decisionEngine({
  alpha,
  sigma,
  confidence,
  drift,
  threshold = 0.7
}) {
  // 1. coherence check
  const coherent = confidence >= threshold;

  // 2. stability check
  const stable = Math.abs(drift ?? 0) < 0.15;

  // 3. signal integrity
  const validSignal =
    alpha !== null &&
    sigma !== null &&
    !Number.isNaN(alpha) &&
    !Number.isNaN(sigma);

  // 4. final decision
  if (!validSignal) {
    return {
      decision: "REJECT",
      reason: "invalid_signal"
    };
  }

  if (!coherent) {
    return {
      decision: "HOLD",
      reason: "low_confidence"
    };
  }

  if (!stable) {
    return {
      decision: "RECALIBRATE",
      reason: "high_drift"
    };
  }

  return {
    decision: "ACCEPT",
    reason: "coherent_stable_signal"
  };
}
