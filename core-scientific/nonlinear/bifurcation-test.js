import { logisticMap } from "./logistic-map.js";
import { computeLyapunov } from "./lyapunov.js";

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function variance(arr, m) {
  return arr.reduce((sum, x) => sum + (x - m) ** 2, 0) / arr.length;
}

export function runBifurcationScan() {

  const results = [];

  for (let r = 2.5; r <= 4.0; r += 0.05) {

    const trajectory = logisticMap(r, 0.5, 2000, 1000);
    const m = mean(trajectory);
    const v = variance(trajectory, m);
    const lyapunov = computeLyapunov(r);

    if (!Number.isFinite(m) || !Number.isFinite(v) || !Number.isFinite(lyapunov)) {
      throw new Error("Numerical instability detected in nonlinear layer.");
    }

    results.push({
      r: Number(r.toFixed(2)),
      mean: m,
      variance: v,
      lyapunov
    });
  }

  return results;
  }
