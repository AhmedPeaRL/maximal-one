export function decisionEngine({ alpha, sigma, confidence, drift }) {
  let action = "HOLD";

  if (confidence > 0.8 && drift < 0.15) {
    action = "BUY";
  } else if (confidence < 0.25 && drift > 0.6) {
    action = "SELL";
  }

  return {
    action,
    asset: "EGX30",
    confidence,
    risk: {
      max_position: 0.05,   // 5%
      stop_loss: 0.02,      // 2%
      take_profit: 0.04     // 4%
    }
  };
}
