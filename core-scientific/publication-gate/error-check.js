export function enforceRelativeError(values) {
  const theoreticalMean = 0.5;
  const epsilon = 1e-8;

  const mean =
    values.reduce((a, b) => a + b, 0) / values.length;

  const variance =
    values.reduce((acc, v) => acc + (v - mean) ** 2, 0) /
    values.length;

  console.log("Empirical mean:", mean);
  console.log("Empirical variance:", variance);

  const error =
    Math.abs(mean - theoreticalMean) /
    Math.max(Math.abs(theoreticalMean), epsilon);

  console.log("Relative mean error:", error);

  if (error >= 0.01) {
    throw new Error(`Relative mean error too high: ${error}`);
  }

  return {
    relativeError: error,
    empiricalMean: mean,
    variance,
    passed: true
  };
}
