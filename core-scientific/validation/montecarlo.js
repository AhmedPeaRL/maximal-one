import { computeTemporalPresence } from "../kernel/temporal-model.js";

function seededRandom(seed) {
  let x = Math.sin(seed) * 10000;
  return function () {
    x = Math.sin(x) * 10000;
    return x - Math.floor(x);
  };
}

function randomEvents(n = 100, seed = 42) {
  const rand = seededRandom(seed);
  const events = [];
  let time = 1000000;

  for (let i = 0; i < n; i++) {
    time += rand() * 1000;
    events.push({
      timestamp: time,
      weight: rand() * 2 - 1
    });
  }

  return events;
}

export function monteCarloTest(iterations = 200) {
  const results = [];

  for (let i = 0; i < iterations; i++) {
    const events = randomEvents(200, i + 1);
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
