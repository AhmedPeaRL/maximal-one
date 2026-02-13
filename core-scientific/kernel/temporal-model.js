const DECAY_LAMBDA = 0.001; // adjust experimentally

function decayFactor(deltaSeconds) {
  return Math.exp(-DECAY_LAMBDA * deltaSeconds);
}

export function computeTemporalPresence(events, lambda = 0.001) {
  if (!events || events.length === 0) return 0;

  let presence = 0;
  let lastTime = events[0].timestamp;

  for (const event of events) {
    const dt = (event.timestamp - lastTime) / 1000;
    const decay = Math.exp(-lambda * dt);

    presence = presence * decay + event.weight;
    lastTime = event.timestamp;
  }

  return presence;
}
