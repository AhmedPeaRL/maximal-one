export function detectExplosion(values) {
  const max = Math.max(...values);

  if (!Number.isFinite(max) || max > 1e9) {
    throw new Error("Numerical explosion detected.");
  }

  return {
    maxValue: max,
    passed: true
  };
}
