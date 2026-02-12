const DECAY_LAMBDA = 0.001; // adjust experimentally

function decayFactor(deltaSeconds) {
  return Math.exp(-DECAY_LAMBDA * deltaSeconds);
}

function computeTemporalPresence(events) {
  if (!events.length) {
    return { presence: 0, residue: 0, silence: true };
  }

  events.sort((a, b) => a.timestamp - b.timestamp);

  let presence = 0;
  let residue = 0;
  let lastTime = events[0].timestamp;

  events.forEach(event => {
    const deltaSeconds = (event.timestamp - lastTime) / 1000;

    presence = presence * decayFactor(deltaSeconds) + event.weight;
    residue += Math.log(1 + event.weight);

    lastTime = event.timestamp;
  });

  return {
    presence,
    residue,
    silence: presence < 25
  };
}
