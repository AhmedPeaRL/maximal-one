export function enforceRelativeError(values) {
  const theoreticalMean = 0.5; // for Uniform(0,1)
  const epsilon = 1e-8;

  const mean =
    values.reduce((a, b) => a + b, 0) / values.length;

  const error =
    Math.abs(mean - theoreticalMean) /
    Math.max(Math.abs(theoreticalMean), epsilon);

  if (error >= 0.01) {
    throw new Error(`Relative mean error too high: ${error}`);
  }

  return {
    relativeError: error,
    empiricalMean: mean,
    passed: true
  };
}
