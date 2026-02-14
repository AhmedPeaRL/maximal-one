import { logisticMap } from "./logistic-map.js";

export function computeLyapunov(r, x0 = 0.5, iterations = 2000, discard = 100) {
  let x = x0;
  let sum = 0;
  let count = 0;

  for (let i = 0; i < iterations; i++) {
    x = r * x * (1 - x);

    if (i >= discard) {
      const derivative = Math.abs(r * (1 - 2 * x));
      if (derivative === 0) continue;
      sum += Math.log(derivative);
      count++;
    }
  }

  return sum / count;
}
