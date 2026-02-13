export function enforceRelativeError(values) {
  const reference = values[0];

  const maxError = Math.max(
    ...values.map(v => Math.abs((v - reference) / reference))
  );

  if (maxError >= 0.01) {
    throw new Error(`Relative error too high: ${maxError}`);
  }

  return {
    relativeError: maxError,
    passed: true
  };
}
