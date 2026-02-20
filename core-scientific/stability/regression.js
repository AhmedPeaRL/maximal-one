function linearRegressionSlope(values) {
  if (!values || values.length < 2) return 0;

  const n = values.length;

  const xs = Array.from({ length: n }, (_, i) => i);
  const meanX = xs.reduce((a, b) => a + b, 0) / n;
  const meanY = values.reduce((a, b) => a + b, 0) / n;

  let numerator = 0;
  let denominator = 0;

  for (let i = 0; i < n; i++) {
    numerator += (xs[i] - meanX) * (values[i] - meanY);
    denominator += Math.pow(xs[i] - meanX, 2);
  }

  return denominator === 0 ? 0 : numerator / denominator;
}

module.exports = { linearRegressionSlope };
