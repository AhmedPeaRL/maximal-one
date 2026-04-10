export async function liveStream(updateFn) {
  let lastHash = null;

  async function tick() {
    try {
      const res = await fetch('./data/live_field_state.json');
      const text = await res.text();

      const hash = await crypto.subtle.digest(
        "SHA-256",
        new TextEncoder().encode(text)
      );

      const hex = Array.from(new Uint8Array(hash))
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");

      if (hex !== lastHash) {
        lastHash = hex;
        const data = JSON.parse(text);
        updateFn(data);
      }

    } catch {}

    requestAnimationFrame(tick);
  }

  tick();
}
