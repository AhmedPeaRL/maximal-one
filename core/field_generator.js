// field_generator.js
// Generates structural numeric field from DOM

(function () {

  function numericField(str) {
    let arr = [];
    for (let i = 0; i < str.length; i++) {
      arr.push(str.charCodeAt(i) % 97);
    }
    return arr;
  }

  function mean(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }

  function variance(arr, m) {
    return arr.reduce((a, b) => a + (b - m) ** 2, 0) / arr.length;
  }

  function generateField() {
    const dom = document.documentElement.outerHTML;
    const field = numericField(dom);
    const m = mean(field);
    const v = variance(field, m);

    const payload = {
      timestamp: new Date().toISOString(),
      length: field.length,
      mean: m,
      variance: v
    };

    console.log("MAXIMAL_FIELD:", JSON.stringify(payload));
    return payload;
  }

  window.addEventListener("load", function () {
    generateField();
  });

})();
