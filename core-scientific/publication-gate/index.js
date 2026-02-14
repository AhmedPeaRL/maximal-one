import { enforceMeanError } from "./error-check.js";
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
import { createSeededRandom } from "../utils/seeded-rng.js";
import fs from "fs";

const random = createSeededRandom(42);
const stress = process.env.STRESS === "true";
const snapshotPath =
  "./core-scientific/publication-gate/snapshot-baseline.json";

export function publicationGate() {
  
  const seed = 999;
  
  const events = stress
  ? randomEvents(5000, seed)
  : randomEvents(10000, seed);

  const empiricalMean =
  events.reduce((a, b) => a + b, 0) / events.length;

  const theoreticalMean = 0; // أو القيمة النظرية الحقيقية لو مختلفة

  const horizon = stress ? 20000 : 5000;

  const report = {
    seed,
    errorCheck: enforceMeanError(empiricalMean, theoreticalMean, 0.01),
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

  report.environment = {
  node: process.version,
  platform: process.platform,
  arch: process.arch
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
    console.log("Mean error:", result.errorCheck);
    console.log(result);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}
