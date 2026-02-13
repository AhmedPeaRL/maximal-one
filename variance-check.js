import { monteCarloTest } from "../validation/montecarlo.js";

export function enforceVariance() {
  const result = monteCarloTest();

  if (result.variance === 0) {
    throw new Error("Variance is zero. Model may be deterministic or broken.");
  }

  return result;
}
