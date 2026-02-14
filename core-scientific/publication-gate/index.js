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

const stress = process.env.STRESS === "true";
const snapshotPath =
  "./core-scientific/publication-gate/snapshot-baseline.json";

export function publicationGate() {
  const events = stress
  ? randomEvents(5000, seed)
  : randomEvents(1000, seed);

  const horizon = stress ? 20000 : 5000;

  const report = {
    seed,
    errorCheck: enforceRelativeError(events),
    varianceCheck: enforceVariance(events),
    stabilityCheck: detectExplosion(events),
    sensitivityCheck: enforceSensitivity(),
    longRunCheck: enforceLongRun(horizon),
    multiSeedCheck: enforceMultiSeed(),
    envelopeCheck: enforceEnvelope(events),
    snapshotCheck: enforceSnapshot(events, seed),
    confidenceCheck: enforceConfidence(events),
    status: "PASSED"
  };
  
  const commitHash = execSync("git rev-parse HEAD")
  .toString()
  .trim();

  report.evolution = recordEvolution(commitHash, report);

  fs.writeFileSync(
  "./core-scientific/publication-gate/report.json",
  JSON.stringify(report, null, 2)
);
  report.environment = {
  node: process.version,
  platform: process.platform,
  arch: process.arch
};
  
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
