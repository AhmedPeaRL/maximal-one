// System Pattern Observatory - Metrics Collector
// Deterministic logging - no randomness injected

(function () {

  const startTime = performance.now();

  function entropy(str) {
    const map = {};
    for (let i = 0; i < str.length; i++) {
      map[str[i]] = (map[str[i]] || 0) + 1;
    }
    let result = 0;
    const len = str.length;
    for (let key in map) {
      const p = map[key] / len;
      result -= p * Math.log2(p);
    }
    return result;
  }

  function collectMetrics() {
    const endTime = performance.now();
    const duration = endTime - startTime;

    const domContent = document.documentElement.innerText;
    const domEntropy = entropy(domContent);

    const metric = {
      timestamp: new Date().toISOString(),
      loadDurationMs: duration,
      domLength: domContent.length,
      domEntropy: domEntropy
    };

    console.log("SPO_METRIC:", JSON.stringify(metric));
    return metric;
  }

  window.addEventListener("load", function () {
    collectMetrics();
  });

})();
