import report from "./report.json" assert { type: "json" };

function assertCondition(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

// 1. Relative Error Check
assertCondition(
  typeof report.relativeError === "number",
  "relativeError missing"
);

assertCondition(
  report.relativeError < 0.01,
  "Relative error exceeds 1%"
);

// 2. Variance Check
assertCondition(
  typeof report.variance === "number",
  "variance missing"
);

assertCondition(
  report.variance !== 0,
  "Variance is zero — model is degenerate"
);

// 3. Sensitivity Stability
assertCondition(
  typeof report.sensitivityDrift === "number",
  "sensitivityDrift missing"
);

assertCondition(
  Math.abs(report.sensitivityDrift) < 0.001,
  "Sensitivity drift unstable"
);

// 4. Numerical Explosion Guard
assertCondition(
  Number.isFinite(report.maxIntermediateValue),
  "Numerical instability detected"
);

console.log("Numerical stability verified.");
