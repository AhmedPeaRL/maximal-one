import { computeTemporalPresence } from "../kernel/temporal-model.js";

function randomEvents(n = 100) {
  const events = [];
  let time = Date.now();

  for (let i = 0; i < n; i++) {
    time += Math.random() * 1000;
    events.push({
      timestamp: time,
      weight: Math.random() * 2 - 1
    });
  }

  return events;
}

export function monteCarloTest(iterations = 500) {
  const results = [];

  for (let i = 0; i < iterations; i++) {
    const events = randomEvents();
    const value = computeTemporalPresence(events);
    results.push(value);
  }

  const mean =
    results.reduce((a, b) => a + b, 0) / results.length;

  const variance =
    results.reduce((a, b) => a + (b - mean) ** 2, 0) /
    results.length;

  return {
    mean,
    variance,
    stdDev: Math.sqrt(variance)
  };
}
