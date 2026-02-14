import { randomEvents } from "../validation/montecarlo.js";
import { enforceMeanError } from "./error-check.js";
import { enforceVariance } from "./variance-check.js";
import { detectExplosion } from "./stability-check.js";

export function enforceMultiSeed() {
  const seeds = [1, 42, 123, 999, 2026, 7777];
  const results = [];

  for (const seed of seeds) {
    const events = randomEvents(200, seed);

    const error = enforceMeanError(empiricalMean, theoreticalMean, 0.01);
    const variance = enforceVariance(events);
    const stability = detectExplosion(events);

    if (!error.passed || !variance.passed || !stability.passed) {
      throw new Error(`Multi-seed failure at seed ${seed}`);
    }

    results.push({ seed, error, variance, stability });
  }

  return {
    testedSeeds: seeds.length,
    passed: true
  };
}
