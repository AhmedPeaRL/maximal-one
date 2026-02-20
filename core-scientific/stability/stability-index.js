function stabilityIndex({ slope, drift, stdDev }) {
  const slopeFactor = Math.min(Math.abs(slope), 1);
  const driftFactor = Math.min(drift, 1);
  const stdFactor = Math.min(stdDev, 1);

  const instability = (slopeFactor + driftFactor + stdFactor) / 3;

  return 1 - instability;
}

module.exports = { stabilityIndex };
