function computeEventRate(events) {
  if (events.length < 2) return 0;

  const sorted = events.sort((a, b) => a.timestamp - b.timestamp);
  const durationSeconds =
    (sorted[sorted.length - 1].timestamp - sorted[0].timestamp) / 1000;

  return durationSeconds > 0 ? events.length / durationSeconds : events.length;
}

function computeAverageWeight(events) {
  if (!events.length) return 0;
  return events.reduce((sum, e) => sum + e.weight, 0) / events.length;
}

function steadyState(rate, avgWeight, lambda) {
  return (rate * avgWeight) / lambda;
}
