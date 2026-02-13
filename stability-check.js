import { sensitivityScan } from "../validation/sensitivity.js";

export function detectExplosion(events) {
  const results = sensitivityScan(events);

  for (const r of results) {
    if (!Number.isFinite(r.value) || Math.abs(r.value) > 1e9) {
      throw new Error(
        `Numerical instability at lambda=${r.lambda}`
      );
    }
  }

  return results;
}
