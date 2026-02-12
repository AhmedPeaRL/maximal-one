async function generateCanonicalSnapshot() {
  const events = await fetchAllWitnessEvents();

  const state = computeTemporalPresence(events);

  const canonicalString = JSON.stringify({
    events: events.sort((a, b) => a.id.localeCompare(b.id)),
    state
  });

  const encoder = new TextEncoder();
  const data = encoder.encode(canonicalString);

  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

  return {
    state,
    hash: hashHex
  };
}
