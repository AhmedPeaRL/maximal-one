export function applyField(signal) {
  const intensity = Math.min(1, signal.velocity + signal.timeOnPage / 60000);
  document.body.style.backgroundColor =
    `rgba(10,10,10,${1 - intensity})`;
  return intensity;
}
