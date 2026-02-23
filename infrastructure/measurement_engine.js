// measurement_engine.js
// STRICTLY ISOLATED FROM EXPRESSION LAYER

(function () {

  const SAMPLE_INTERVAL = 20000;

  function computeEntropy(str) {
    const freq = {};
    for (let i = 0; i < str.length; i++) {
      freq[str[i]] = (freq[str[i]] || 0) + 1;
    }

    let entropy = 0;
    const len = str.length;

    for (let k in freq) {
      const p = freq[k] / len;
      entropy -= p * Math.log2(p);
    }

    return entropy;
  }

  async function measure() {
    const t0 = performance.now();

    try {
      await fetch(window.location.href, { cache: "no-store" });
    } catch (e) {
      return;
    }

    const t1 = performance.now();
    const latency = t1 - t0;

    const dom = document.documentElement.outerHTML;
    const entropy = computeEntropy(dom);

    const payload = {
      timestamp: Date.now(),
      latency: latency,
      entropy: entropy,
      domLength: dom.length
    };

    console.log("HCM_MEASURE:", JSON.stringify(payload));
  }

  setInterval(measure, SAMPLE_INTERVAL);

})();
