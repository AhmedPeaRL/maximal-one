import { computeTemporalPresence } from "../kernel/temporal-model.js";

function numericalIntegration(events, lambda) {
  let presence = 0;
  let lastTime = events[0]?.timestamp || 0;

  for (const event of events) {
    const dt = (event.timestamp - lastTime) / 1000;

    // Approximate decay using Taylor expansion (independent method)
    const decayApprox = 1 - lambda * dt + 0.5 * (lambda * dt) ** 2;

    presence = presence * decayApprox + event.weight;

    lastTime = event.timestamp;
  }

  return presence;
}

export function falsificationTest(events, lambda) {
  const model = computeTemporalPresence(events);
  const numerical = numericalIntegration(events, lambda);

  const error = Math.abs(model - numerical);

  return {
    model,
    numerical,
    error,
    relativeError: error / (numerical || 1)
  };
}
