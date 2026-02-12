export function applyDynamics(signal) {
  const factor = Math.min(1, signal.velocity + signal.time / 60000);
  document.documentElement.style.setProperty(
    "--field-opacity",
    1 - factor
  );
  return factor;
}
