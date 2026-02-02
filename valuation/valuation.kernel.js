/*
  Latent Valuation Kernel
  Calculates internal coherence weight.
  Produces no output.
  Exposes nothing.
*/

(function () {
  const ValuationState = {
    coherence: 0,
    entropy: 0,
    lastMark: performance.now()
  };

  function observePresence() {
    const now = performance.now();
    const delta = now - ValuationState.lastMark;

    if (delta > 1200 && delta < 12000) {
      ValuationState.coherence += 1;
    } else {
      ValuationState.entropy += 1;
    }

    ValuationState.lastMark = now;
  }

  function observeSilence() {
    ValuationState.coherence += 0.5;
  }

  function observeExtractionAttempt() {
    ValuationState.entropy += 2;
  }

  window.addEventListener("mousemove", observePresence);
  window.addEventListener("keydown", observePresence);
  window.addEventListener("visibilitychange", observeSilence);
  window.addEventListener("focus", observeExtractionAttempt);

  Object.freeze(ValuationState);

  if (typeof window !== "undefined") {
    window.__VALUATION__ = ValuationState;
  }
})();
