import { Rhythm } from "./rhythm.js";

window.addEventListener("mousemove", () => {
  Rhythm.state = "disturbed";
  Rhythm.observe();
});

import { VoiceGate } from "./voice-gate.js";

export function delegatePresenceSignal(signal, source) {
  return VoiceGate.speak(signal, source);
}

window.__SOVEREIGN_WITNESS__ = witness;
