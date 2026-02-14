import { createSeededRandom } from "../utils/seeded-random.js";

export function runEmpiricalValidation() {

  const random = createSeededRandom(42);
  const sampleSize = 10000;
  const theoreticalMean = 0.5;

  let sum = 0;
  let sumSquares = 0;

  for (let i = 0; i < sampleSize; i++) {
    const x = random();

    // Guard against floating overflow (future scaling safety)
    if (!Number.isFinite(x)) {
      throw new Error("Non-finite random sample detected");
    }

    sum += x;
    sumSquares += x * x;
  }

  const empiricalMean = sum / sampleSize;
  const variance = (sumSquares / sampleSize) - empiricalMean ** 2;

  if (variance <= 0 || !Number.isFinite(variance)) {
    throw new Error("Numerical instability in variance computation");
  }

  const empiricalStd = Math.sqrt(variance);
  const relativeError = Math.abs(empiricalMean - theoreticalMean) / theoreticalMean;

  return {
    empiricalMean,
    theoreticalMean,
    empiricalStd,
    sampleSize,
    relativeError
  };
}
