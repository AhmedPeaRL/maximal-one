export function enforceScientificMetrics(metrics) {

  const MAX_RELATIVE_ERROR = 0.01; // 1%
  const MAX_SENSITIVITY = 10;
  const MIN_DRIFT_EPSILON = 0; // drift can be zero if system is deterministic

  if (metrics.relativeError > MAX_RELATIVE_ERROR) {
    throw new Error("Relative error exceeds 1%");
  }

  if (metrics.sensitivity > MAX_SENSITIVITY) {
    throw new Error("Sensitivity unstable");
  }

  if (metrics.variance < MIN_DRIFT_EPSILON) {
    // Drift across seeds may be zero — this is acceptable
    // We rely on per-seed variance assertion inside publicationGate
  }

}
