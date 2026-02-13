import { computeTemporalPresence } from "../kernel/temporal-model.js";

export function stabilityMap(events) {
  const lambdas = [];
  for (let i = 0.0001; i <= 0.02; i += 0.0005) {
    lambdas.push(i);
  }

  return lambdas.map(lambda => {
    const value = computeTemporalPresence(events, lambda);
    return { lambda, value };
  });
}
