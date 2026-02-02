/*
 IRREVERSIBLE ADDRESSABILITY
 Words enter. Text never remains.
*/

(function () {

  const KEY = "__MAXIMAL_ADDRESS_WEIGHT__";
  const root = document.documentElement;

  let weight = 0;

  function load() {
    try {
      weight = parseFloat(localStorage.getItem(KEY)) || 0;
    } catch (_) {}
  }

  function save() {
    localStorage.setItem(KEY, weight.toString());
  }

  function absorb(text) {
    const density = text.trim().length;
    if (!density) return;

    weight += Math.sqrt(density) * 0.73;
    distort();
    save();
  }

  function distort() {
    const scale = 1 + Math.min(0.18, weight * 0.00012);
    const blur = Math.min(0.6, weight * 0.00025);

    root.style.transform = `scale(${scale})`;
    root.style.filter = `blur(${blur}px) contrast(${scale})`;
  }

  // exposed but never documented
  window.__ADDRESS__ = function (text) {
    absorb(text);
  };

  load();
  distort();

})();
