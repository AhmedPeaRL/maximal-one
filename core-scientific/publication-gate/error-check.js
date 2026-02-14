export function enforceRelativeError(values) {
  const lambda = 0.01;
  const epsilon = 1e-8; // threshold to avoid division near zero

  let maxError = 0;

  for (let i = 0; i < values.length; i++) {
    const theoretical = Math.exp(-lambda * i);

    if (Math.abs(theoretical) < epsilon) {
      continue; // ignore unstable tail region
    }

    const error =
      Math.abs(values[i] - theoretical) /
      Math.abs(theoretical);

    if (error > maxError) {
      maxError = error;
    }
  }

  if (maxError >= 0.01) {
    throw new Error(`Relative error too high: ${maxError}`);
  }

  return {
    relativeError: maxError,
    passed: true
  };
}
