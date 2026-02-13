import { enforceRelativeError } from "./error-check.js";
import { enforceVariance } from "./variance-check.js";
import { detectExplosion } from "./stability-check.js";
import { enforceSensitivity } from "./sensitivity-check.js";
import { enforceLongRun } from "./long-run-check.js";
import { randomEvents } from "../validation/montecarlo.js";
import fs from "fs";

export function publicationGate() {
  const seed = 999;
  const events = randomEvents(200, seed);

  const report = {
    seed,
    errorCheck: enforceRelativeError(events),
    varianceCheck: enforceVariance(events),
    stabilityCheck: detectExplosion(events),
    sensitivityCheck: enforceSensitivity(),
    longRunCheck: enforceLongRun(),
    status: "PASSED"
  };

  fs.writeFileSync(
    "./core-scientific/publication-gate/report.json",
    JSON.stringify(report, null, 2)
  );

  return report;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const result = publicationGate();
    console.log(result);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}
