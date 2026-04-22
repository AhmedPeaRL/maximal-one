export function irreversibleDecisionEngine(signal) {
  const { alpha, sigma, confidence, drift } = signal;

  let decision = "HOLD";
  let irreversible = false;

  if (confidence > 0.85 && sigma < 0.2 && Math.abs(drift) < 0.1) {
    decision = "COMMIT";
    irreversible = true;
  }

  if (sigma > 0.3 || drift > 0.5) {
    decision = "REJECT";
    irreversible = true;
  }

  return {
    decision,
    irreversible,
    timestamp: Date.now(),
    reason: {
      alpha,
      sigma,
      confidence,
      drift
    }
  };
}
