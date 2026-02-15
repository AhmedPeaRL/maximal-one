export function enforceScientificMetrics(report) {

  const MAX_RELATIVE_ERROR = 0.01; // 1%
  const MIN_VARIANCE = 1e-12;
  const MAX_SENSITIVITY = 10;

  if (report.relativeError > MAX_RELATIVE_ERROR) {
    throw new Error("Relative error exceeds 1%");
  }

  if (report.variance <= MIN_VARIANCE) {
    throw new Error("Variance is zero or numerically collapsed");
  }

  if (report.sensitivity > MAX_SENSITIVITY) {
    throw new Error("Sensitivity unstable");
  }

}
