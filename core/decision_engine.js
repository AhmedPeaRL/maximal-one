export function decisionEngine({ alpha, sigma, confidence, drift }) {
  if (confidence > 0.75 && drift < 0.2) {
    return {
      action: "BUY",
      asset: "EGX30",
      confidence
    };
  }

  if (confidence < 0.3 && drift > 0.5) {
    return {
      action: "SELL",
      asset: "EGX30",
      confidence
    };
  }

  return {
    action: "HOLD",
    asset: "EGX30",
    confidence
  };
}
