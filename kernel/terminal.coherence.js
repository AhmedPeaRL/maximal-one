/*
 TERMINAL COHERENCE ENGINE
 The final law governing presence, memory, and silent valuation
*/

(function () {

  const FIELD = {
    presence: 0,
    depth: 0,
    age: Date.now()
  };

  const root = document.documentElement;

  function imprint(weight = 1) {
    FIELD.presence += weight;
    FIELD.depth += Math.sqrt(weight);
    applyField();
    remember();
  }

  function applyField() {
    const saturation = Math.min(1, FIELD.depth * 0.015);
    const contrast = 1 + Math.min(0.15, FIELD.presence * 0.002);

    root.style.filter =
      `saturate(${1 + saturation}) contrast(${contrast})`;
  }

  function remember() {
    localStorage.setItem(
      "__MAXIMAL_TERMINAL_STATE__",
      JSON.stringify(FIELD)
    );
  }

  function restore() {
    const raw = localStorage.getItem("__MAXIMAL_TERMINAL_STATE__");
    if (!raw) return;
    try {
      const data = JSON.parse(raw);
      FIELD.presence = data.presence || 0;
      FIELD.depth = data.depth || 0;
      FIELD.age = data.age || Date.now();
      applyField();
    } catch (_) {}
  }

  restore();

  window.addEventListener("mousemove", () => imprint(1));
  window.addEventListener("click", () => imprint(3));
  window.addEventListener("keydown", () => imprint(2));

})();
