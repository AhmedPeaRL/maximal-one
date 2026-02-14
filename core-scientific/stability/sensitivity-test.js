import { createSeededRNG } from "../utils/seeded-rng.js";

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function std(arr, m) {
  const variance =
    arr.reduce((sum, x) => sum + (x - m) ** 2, 0) /
    arr.length;
  return Math.sqrt(variance);
}

function simulate(seed, sampleSize) {
  const rng = createSeededRNG(seed);
  const values = [];

  for (let i = 0; i < sampleSize; i++) {
    values.push(rng() * 2 - 1);
  }

  const m = mean(values);
  const s = std(values, m);

  return { mean: m, std: s };
}

export function runSensitivitySuite() {
  const configs = [
    { seed: 42, n: 10000 },
    { seed: 43, n: 10000 },
    { seed: 44, n: 10000 },
    { seed: 42, n: 5000 },
    { seed: 42, n: 20000 }
  ];

  const results = configs.map(cfg => ({
    ...cfg,
    ...simulate(cfg.seed, cfg.n)
  }));

  const unstable = results.some(r => Math.abs(r.mean) > 0.02);

  if (unstable) {
    throw new Error("Sensitivity instability detected.");
  }

  return results;
}
