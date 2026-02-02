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
