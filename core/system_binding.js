export function bindSystemLayers(input, state, analysis) {
  return {
    input,
    state,
    analysis,
    timestamp: Date.now(),
    coherence: computeCoherence(input, state, analysis)
  };
}

function computeCoherence(i, s, a) {
  try {
    const raw = JSON.stringify({ i, s, a });
    let hash = 0;

    for (let j = 0; j < raw.length; j++) {
      hash = (hash << 5) - hash + raw.charCodeAt(j);
      hash |= 0;
    }

    return Math.abs(hash);
  } catch {
    return 0;
  }
}
