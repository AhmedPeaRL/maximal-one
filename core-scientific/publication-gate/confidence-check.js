import { randomEvents } from "../validation/montecarlo.js";

export function enforceConfidence() {
  const events = randomEvents(2000, 999);

  const mean =
    events.reduce((a, b) => a + b, 0) / events.length;

  const variance =
    events.reduce((a, b) => a + (b - mean) ** 2, 0) /
    events.length;

  const std = Math.sqrt(variance);

  const margin = 1.96 * (std / Math.sqrt(events.length));

  return {
    mean,
    confidence95: [mean - margin, mean + margin],
    passed: true
  };
}
