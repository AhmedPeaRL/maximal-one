import { randomEvents } from "../validation/montecarlo.js";

export function enforceLongRun() {
  const events = randomEvents(5000, 999);

  const max = Math.max(...events);

  if (!Number.isFinite(max) || max > 10) {
    throw new Error("Long run instability detected.");
  }

  return {
    horizon: 5000,
    maxObserved: max,
    passed: true
  };
}
