// core/time_probe.js

(function () {

  function sample() {
    return performance.now() % 1000;
  }

  window.TimeProbe = { sample };
  
(function () {

  function probe() {
    const now = Date.now();
    const phase = now % 100000;

    const payload = {
      timestamp: new Date().toISOString(),
      epochMod: phase
    };

    console.log("TIME_PROBE:", JSON.stringify(payload));
  }

  setInterval(probe, 10000);

})();
