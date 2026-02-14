export function enforceMeanError(empiricalMean, theoreticalMean, tolerance = 0.01) {
  const epsilon = 1e-8;

  const absError = Math.abs(empiricalMean - theoreticalMean);

  if (Math.abs(theoreticalMean) < epsilon) {
    // Use absolute error when theoretical mean is near zero
    if (absError > tolerance) {
      throw new Error(`Absolute mean error too high: ${absError}`);
    }
    return absError;
  }

  const relativeError = absError / Math.abs(theoreticalMean);

  if (relativeError > tolerance) {
    throw new Error(`Relative mean error too high: ${relativeError}`);
  }

  return relativeError;
}
