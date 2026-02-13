import fs from "fs";
import { randomEvents } from "../validation/montecarlo.js";

export function enforceSnapshot() {
  const seed = 999;
  const events = randomEvents(50, seed);

  const snapshotPath =
    "./core-scientific/publication-gate/baseline-snapshot.json";

  if (!fs.existsSync(snapshotPath)) {
    fs.writeFileSync(
      snapshotPath,
      JSON.stringify(events, null, 2)
    );
    return { createdBaseline: true };
  }

  const baseline = JSON.parse(
    fs.readFileSync(snapshotPath)
  );

  const identical =
    JSON.stringify(events) === JSON.stringify(baseline);

  if (!identical) {
    throw new Error("Deterministic snapshot mismatch.");
  }

  return { snapshotMatch: true };
}
