import { computeTemporalPresence } from "../kernel/temporal-model.js";

export function sensitivityScan(events) {
  const lambdas = [0.0005, 0.001, 0.002, 0.005, 0.01];
  return lambdas.map(lambda => ({
    lambda,
    value: computeTemporalPresence(events, lambda)
  }));
}
