export function disturbance(signal) {
  return Math.min(1, signal.intensity * 1.3);
}
