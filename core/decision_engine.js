export function decisionEngine({
  alpha,
  sigma,
  confidence,
  drift
}) {
  return {
    action: "OBSERVE",
    asset: null,
    alpha,
    sigma,
    confidence,
    drift,
    epistemic_policy: {
      market_execution_enabled: false,
      trading_authorization: false,
      scientific_output_authorizes_financial_action: false
    }
  };
}
