import { randomEvents } from "../validation/montecarlo.js";

export function enforceSensitivity(count = 200) {
  const base = randomEvents(count, 999);
  const perturbed = randomEvents(count, 1000);

  let divergence = 0;

  for (let i = 0; i < count; i++) {
    divergence += Math.abs(base[i] - perturbed[i]);
  }

  divergence /= count;

  if (divergence > 0.01) {
    throw new Error(`Sensitivity instability detected: ${divergence}`);
  }

  return {
    averageDivergence: divergence,
    passed: true
  };
}
