import { randomEvents } from "../validation/montecarlo.js";

export function enforceEnvelope() {
  const events = randomEvents(1000, 999);

  const mean =
    events.reduce((a, b) => a + b, 0) / events.length;

  const variance =
    events.reduce((a, b) => a + (b - mean) ** 2, 0) /
    events.length;

  if (mean < 0 || mean > 1) {
    throw new Error("Mean outside expected envelope.");
  }

  if (variance <= 0 || variance > 1) {
    throw new Error("Variance outside expected envelope.");
  }

  return {
    mean,
    variance,
    passed: true
  };
}
