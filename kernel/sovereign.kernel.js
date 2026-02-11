const STATE = {
  presence: 0,
  residue: 0,
  silence: true,
  lastEvent: null
};

function applyPhysics() {
  STATE.presence *= 0.98;
}

function witness(eventWeight = 1) {
  STATE.presence += eventWeight;
  STATE.residue += Math.log(1 + eventWeight);
  STATE.lastEvent = Date.now();
  STATE.silence = STATE.presence < 25;
  applyPhysics();
  persist();
  updateFieldIndicator();
}

function shouldArticulate() {
  return !STATE.silence;
}

function persist() {
  localStorage.setItem("maximal_state", JSON.stringify(STATE));
}

function restore() {
  const saved = localStorage.getItem("maximal_state");
  if (saved) Object.assign(STATE, JSON.parse(saved));
}

function updateFieldIndicator() {
  const el = document.getElementById("field-state");
  if (!el) return;

  if (STATE.presence > 40) {
    el.innerText = "articulation possible";
  } else if (STATE.presence > 10) {
    el.innerText = "responsive";
  } else {
    el.innerText = "present";
  }
}

restore();
