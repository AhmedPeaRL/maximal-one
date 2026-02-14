export function enforceMeanError(
  empiricalMean,
  theoreticalMean,
  tolerance,
  empiricalStd,
  sampleSize
) {
  const absoluteError = Math.abs(
    empiricalMean - theoreticalMean
  );

  // === Dynamic tolerance fallback ===
  // If empiricalStd and sampleSize provided, compute 3-sigma bound
  let effectiveTolerance = tolerance;

  if (empiricalStd && sampleSize) {
    effectiveTolerance =
      (3 * empiricalStd) / Math.sqrt(sampleSize);
  }

  if (absoluteError > effectiveTolerance) {
    throw new Error(
      `Absolute mean error too high: ${absoluteError} (tolerance: ${effectiveTolerance})`
    );
  }

  return {
    absoluteError,
    tolerance: effectiveTolerance,
    status: "PASSED"
  };
}
