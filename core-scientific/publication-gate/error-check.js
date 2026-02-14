export function enforceMeanError(
  empiricalMean,
  theoreticalMean,
  _tolerance,
  empiricalStd,
  sampleSize
) {
  const absoluteError = Math.abs(
    empiricalMean - theoreticalMean
  );

  const tolerance =
    (3 * empiricalStd) / Math.sqrt(sampleSize);

  if (absoluteError > tolerance) {
    throw new Error(
      `Absolute mean error too high: ${absoluteError} (tolerance: ${tolerance})`
    );
  }

  return {
    absoluteError,
    tolerance,
    status: "PASSED"
  };
}
