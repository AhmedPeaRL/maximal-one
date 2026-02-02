/*
  Digestive Layer
  Converts witnessed presence into internal patterns.
  No rendering.
  No storage.
  No emission.
*/

(function () {
  const DigestiveState = {
    intervals: [],
    silences: 0,
    disturbances: 0,
    lastMark: performance.now()
  };

  function markPresence() {
    const now = performance.now();
    DigestiveState.intervals.push(now - DigestiveState.lastMark);
    DigestiveState.lastMark = now;
  }

  function markSilence() {
    DigestiveState.silences += 1;
  }

  function markDisturbance() {
    DigestiveState.disturbances += 1;
  }

  window.addEventListener("mousemove", markPresence);
  window.addEventListener("keydown", markPresence);
  window.addEventListener("visibilitychange", markSilence);
  window.addEventListener("blur", markDisturbance);

  Object.freeze(DigestiveState);

  if (typeof window !== "undefined") {
    window.__DIGESTION__ = DigestiveState;
  }
})();
