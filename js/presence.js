export function measurePresence() {
  let lastMove = Date.now();
  let velocity = 0;

  window.addEventListener("mousemove", e => {
    const now = Date.now();
    velocity = Math.min(1, (now - lastMove) / 1000);
    lastMove = now;
  });

  return () => ({
    velocity,
    timeOnPage: performance.now()
  });
}
