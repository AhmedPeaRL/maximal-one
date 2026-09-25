export function decisionEngine({
  alpha,
  sigma,
  confidence,
  drift
}) {
  return {
    action: "HOLD",
    asset: "EGX30",
    confidence: null,
    risk: {
      max_position: 0,
      stop_loss: null,
      take_profit: null
    },
    epistemic_policy: {
      scientific_outputs_are_not_trading_authorization: true,
      execution_disabled: true
    }
  };
}
