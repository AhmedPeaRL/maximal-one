export function witness(pulse) {
  return {
    witnessed: true,
    intensity: pulse.intensity,
    at: pulse.timestamp
  };
}
