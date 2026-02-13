export function enforceVariance(values = [1, 2, 3, 4, 5]) {
  const mean =
    values.reduce((a, b) => a + b, 0) / values.length;

  const variance =
    values.reduce((sum, v) => sum + (v - mean) ** 2, 0) /
    values.length;

  if (variance === 0) {
    throw new Error("Variance is zero — system collapsed to fixed state.");
  }

  return {
    variance,
    passed: true
  };
}
