import { computeTemporalPresence } from "../kernel/state-evolution.js";
import { steadyState } from "../analytics/stats.js";

function generateRandomEvents(count, lambda) {
  const events = [];
  let currentTime = 0;

  for (let i = 0; i < count; i++) {
    const delta = -Math.log(Math.random()) / lambda;
    currentTime += delta * 1000;

    events.push({
      id: `sim-${i}`,
      timestamp: currentTime,
      weight: 1
    });
  }

  return events;
}

export function runMonteCarlo(iterations, lambda) {
  const results = [];

  for (let i = 0; i < iterations; i++) {
    const events = generateRandomEvents(500, lambda);
    const simulated = computeTemporalPresence(events);

    const rate = events.length /
      ((events[events.length - 1].timestamp - events[0].timestamp) / 1000);

    const theoretical = steadyState(rate, 1, lambda);

    results.push({
      simulated,
      theoretical,
      error: Math.abs(simulated - theoretical)
    });
  }

  return results;
}
