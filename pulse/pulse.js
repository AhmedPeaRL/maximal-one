export function pulse() {
  return {
    intensity: Math.random(),
    timestamp: Date.now()
  };
}
