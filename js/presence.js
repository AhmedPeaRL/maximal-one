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

export function presenceStream() {
  let last = performance.now();
  let velocity = 0;

  window.addEventListener("mousemove", () => {
    const now = performance.now();
    velocity = Math.min(1, (now - last) / 500);
    last = now;
  });

  return () => ({
    velocity,
    time: performance.now()
  });
}

export function presenceSignal() {
  let last = performance.now();
  let intensity = 0;

  window.addEventListener("mousemove", () => {
    const now = performance.now();
    intensity = Math.min(1, (now - last) / 400);
    last = now;
  });

  return () => ({
    intensity,
    t: performance.now()
  });
}
