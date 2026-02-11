/*
 SOVEREIGN KERNEL — MAXIMAL-ONE
 The single convergent law of presence, witness, and residue
*/

(function () {
  const STATE = {
    presence: 0,
    residue: 0,
    lastEvent: Date.now()
  };

  const body = document.body;

  function updateFieldIndicator() {
  const el = document.getElementById("field-state");
  if (!el) return;

  if (STATE.presence > 50) {
    el.innerText = "deepening";
  } else if (STATE.presence > 10) {
    el.innerText = "responsive";
  } else {
    el.innerText = "present";
  }
}

function witness(eventWeight = 1) {
  STATE.presence += eventWeight;
  STATE.residue += Math.log(1 + eventWeight);
  applyPhysics();
  updateFieldIndicator();
  persist();
}

  function applyPhysics() {
    const glow = Math.min(0.6, STATE.presence * 0.002);
    const blur = Math.min(2, STATE.residue * 0.15);
    body.style.boxShadow = `inset 0 0 120px rgba(255,215,180,${glow})`;
    body.style.filter = `blur(${blur * 0.05}px)`;
  }

  function persist() {
    localStorage.setItem(
      "__MAXIMAL_RESIDUE__",
      JSON.stringify({
        presence: STATE.presence,
        residue: STATE.residue,
        lastEvent: STATE.lastEvent
      })
    );
  }

  function restore() {
    const saved = localStorage.getItem("__MAXIMAL_RESIDUE__");
    if (!saved) return;
    try {
      const parsed = JSON.parse(saved);
      STATE.presence = parsed.presence || 0;
      STATE.residue = parsed.residue || 0;
      STATE.lastEvent = parsed.lastEvent || Date.now();
      applyPhysics();
    } catch (_) {}
  }

  restore();

  window.addEventListener("mousemove", () => witness(1));
  window.addEventListener("click", () => witness(3));
  window.addEventListener("keydown", () => witness(2));
})();
