function computeHalfLife(lambda) {
  return Math.log(2) / lambda;
}

function steadyStateEstimate(rate, avgWeight, lambda) {
  return (rate * avgWeight) / lambda;
}
