(function () {

  async function measure() {
    const start = performance.now();

    try {
      await fetch(window.location.href, { cache: "no-store" });
    } catch (e) {
      return;
    }

    const end = performance.now();
    const latency = end - start;

    const payload = {
      timestamp: Date.now(),
      latency: latency
    };

    console.log("NETWORK_PROBE:", JSON.stringify(payload));
  }

  setInterval(measure, 15000);

})();
