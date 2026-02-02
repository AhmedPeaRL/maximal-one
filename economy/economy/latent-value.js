/*
  Latent Value Observer
  This layer does not output.
  It only witnesses.
*/

(function () {
  const LatentValue = {
    presenceDuration: 0,
    silentMoments: 0,
    revisits: 0,
    lastSeen: Date.now()
  };

  let lastActivity = Date.now();

  function tick() {
    const now = Date.now();
    LatentValue.presenceDuration += now - lastActivity;
    lastActivity = now;
  }

  function silentWitness() {
    LatentValue.silentMoments += 1;
  }

  window.addEventListener("mousemove", tick);
  window.addEventListener("keydown", tick);
  window.addEventListener("visibilitychange", silentWitness);

  if (typeof window !== "undefined") {
    window.__LATENT_VALUE__ = Object.freeze(LatentValue);
  }
})();
