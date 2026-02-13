import { computeTemporalPresence } from "../kernel/temporal-model.js";

function independentApproximation(events, lambda) {
  let presence = 0;
  let lastTime = events[0]?.timestamp || 0;

  for (const event of events) {
    const dt = (event.timestamp - lastTime) / 1000;

    // Independent second-order approximation
    const decay = 1 - lambda * dt + 0.5 * (lambda * dt) ** 2;

    presence = presence * decay + event.weight;
    lastTime = event.timestamp;
  }

  return presence;
}

export function runFalsification(events, lambda = 0.001) {
  const model = computeTemporalPresence(events, lambda);
  const independent = independentApproximation(events, lambda);

  const error = Math.abs(model - independent);
  const relativeError = error / (Math.abs(independent) || 1);

  return {
    model,
    independent,
    error,
    relativeError
  };
}
