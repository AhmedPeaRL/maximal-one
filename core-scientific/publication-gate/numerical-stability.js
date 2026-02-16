const fs = require("fs");

const report = require("./report.json");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

// 1. Relative Error Check
assert(
  report.relativeError < 0.01,
  "Relative error exceeds 1%"
);

// 2. Variance Check
assert(
  report.variance !== 0,
  "Variance is zero — model is degenerate"
);

// 3. Sensitivity Stability
assert(
  Math.abs(report.sensitivityDrift) < 0.001,
  "Sensitivity drift unstable"
);

// 4. Numerical Explosion Guard
assert(
  Number.isFinite(report.maxIntermediateValue),
  "Numerical instability detected"
);

console.log("Numerical stability verified.");
