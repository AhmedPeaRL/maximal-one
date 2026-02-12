export function disturbance(signal) {
  return Math.min(1, signal.intensity * 1.3);
}

export function toDisturbance(signal) {
  return Math.min(1, signal.activity * 1.4);
}
