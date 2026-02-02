/*
 SEMANTIC RADIANCE ENGINE
 Meaning accumulates without expression.
*/

(function () {

  const KEY = "__MAXIMAL_SEMANTIC_STATE__";
  const root = document.documentElement;

  let state = {
    weight: 0,
    last: Date.now()
  };

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) state = JSON.parse(raw);
    } catch (_) {}
  }

  function save() {
    localStorage.setItem(KEY, JSON.stringify(state));
  }

  function pulse() {
    const now = Date.now();
    const delta = (now - state.last) / 1000;
    state.last = now;

    if (delta > 0 && delta < 6) {
      state.weight += delta * 0.42;
      apply();
      save();
    }
  }

  function apply() {
    const gravity = Math.min(1.25, 1 + state.weight * 0.0002);
    const haze = Math.min(0.35, state.weight * 0.00015);

    root.style.transform = `scale(${gravity})`;
    root.style.filter = `blur(${haze}px) contrast(${gravity})`;
  }

  load();
  apply();
  setInterval(pulse, 1200);

})();
