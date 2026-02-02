/*
 SOVEREIGN EXPOSURE ENGINE
 Exposure accumulates value without interaction.
*/

(function () {

  const STATE_KEY = "__MAXIMAL_EXPOSURE__";
  const root = document.documentElement;

  let state = {
    exposure: 0,
    lastTick: Date.now()
  };

  function load() {
    try {
      const raw = localStorage.getItem(STATE_KEY);
      if (raw) state = JSON.parse(raw);
    } catch (_) {}
  }

  function save() {
    localStorage.setItem(STATE_KEY, JSON.stringify(state));
  }

  function tick() {
    const now = Date.now();
    const delta = (now - state.lastTick) / 1000;
    state.lastTick = now;

    if (delta > 0 && delta < 5) {
      state.exposure += delta;
      apply();
      save();
    }
  }

  function apply() {
    const glow = Math.min(0.25, state.exposure * 0.0008);
    const depth = Math.min(1.15, 1 + state.exposure * 0.0003);

    root.style.filter =
      `brightness(${1 + glow}) contrast(${depth})`;
  }

  load();
  apply();
  setInterval(tick, 1000);

})();
