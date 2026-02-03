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
