export function runEmpiricalValidation() {

  const sampleSize = 10000;
  const theoreticalMean = 0.5;

  let sum = 0;
  let sumSquares = 0;

  for (let i = 0; i < sampleSize; i++) {
    const x = Math.random();
    sum += x;
    sumSquares += x * x;
  }

  const empiricalMean = sum / sampleSize;
  const variance = (sumSquares / sampleSize) - empiricalMean ** 2;
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
