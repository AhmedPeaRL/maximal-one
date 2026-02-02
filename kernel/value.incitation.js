/*
 Value Incitation Protocol — MAXIMAL-ONE
 Converts user presence & action into immediate visual "value pulses"
*/

(async function () {
  const ELEMENT_ID = "value-incitation";
  let container = document.getElementById(ELEMENT_ID);
  if (!container) {
    container = document.createElement("div");
    container.id = ELEMENT_ID;
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100%";
    container.style.height = "100%";
    container.style.pointerEvents = "none";
    container.style.zIndex = "9999";
    document.body.appendChild(container);
  }

  function createPulse(intensity = 1) {
    const pulse = document.createElement("div");
    const size = 20 + intensity * 10;
    pulse.style.width = `${size}px`;
    pulse.style.height = `${size}px`;
    pulse.style.borderRadius = "50%";
    pulse.style.position = "absolute";
    pulse.style.left = `${Math.random() * window.innerWidth}px`;
    pulse.style.top = `${Math.random() * window.innerHeight}px`;
    pulse.style.background = `rgba(255,215,0,${0.2 + 0.05*intensity})`;
    pulse.style.pointerEvents = "none";
    pulse.style.transition = "all 1.2s ease-out";
    container.appendChild(pulse);
    setTimeout(() => pulse.remove(), 1200);
  }

  function captureInteraction(e) {
    const intensity = Math.min(5, Math.ceil(Math.random() * 3 + (e.movementX + e.movementY)/100));
    createPulse(intensity);
  }

  window.addEventListener("mousemove", captureInteraction);
  window.addEventListener("keydown", e => createPulse(3));
  window.addEventListener("click", e => createPulse(4));
})();
