import { computeTemporalPresence } from "../kernel/temporal-model.js";

export function sensitivityScan(events) {
  const lambdas = [0.0005, 0.001, 0.002, 0.005];
  const results = [];

  for (const lambda of lambdas) {
    const value = computeTemporalPresence(events, lambda);
    results.push({ lambda, value });
  }

  return results;
}
