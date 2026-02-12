/*
 WITNESS BRIDGE — connects external witness logic to sovereign kernel
*/

window.__WITNESS_SIGNAL__ = function (weight = 1) {
  if (typeof window.dispatchEvent === "function") {
    window.dispatchEvent(
      new CustomEvent("witness-signal", { detail: weight })
    );
  }
};

window.addEventListener("witness-signal", e => {
  if (window.__SOVEREIGN_WITNESS__) {
    window.__SOVEREIGN_WITNESS__(e.detail);
  }
});
