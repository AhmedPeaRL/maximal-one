import { enforceRelativeError } from "./error-check.js";
import { enforceVariance } from "./variance-check.js";
import { detectExplosion } from "./stability-check.js";
import { enforceSensitivity } from "./sensitivity-check.js";
import { enforceLongRun } from "./long-run-check.js";
import { enforceMultiSeed } from "./multiseed-check.js";
import { enforceEnvelope } from "./envelope-check.js";
import { enforceSnapshot } from "./snapshot-check.js";
import { enforceConfidence } from "./confidence-check.js";
import { randomEvents } from "../validation/montecarlo.js";
import { execSync } from "child_process";
import { recordEvolution } from "./evolution-recorder.js";
import fs from "fs";

const snapshotPath =
  "./core-scientific/publication-gate/snapshot-baseline.json";

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
    multiSeedCheck: enforceMultiSeed(),
    envelopeCheck: enforceEnvelope(),
    snapshotCheck: enforceSnapshot(),
    confidenceCheck: enforceConfidence(),
    status: "PASSED"
  };

  snapshotCheck(currentState, seed) {

    if (!fs.existsSync(snapshotPath)) {
    fs.writeFileSync(
      snapshotPath,
      JSON.stringify(currentState, null, 2)
    );
    return { createdBaseline: true };
  }

  const baseline = JSON.parse(
    fs.readFileSync(snapshotPath)
  );

  const match =
    JSON.stringify(baseline) ===
    JSON.stringify(currentState);

  if (!match) {
    throw new Error(
      "Determinism violation: snapshot mismatch under fixed seed"
    );
  }

  return { snapshotMatch: true };
  }
  
  const commitHash = execSync("git rev-parse HEAD")
  .toString()
  .trim();

  report.evolution = recordEvolution(commitHash, report);
  
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
