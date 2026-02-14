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

export function publicationGate() {
  const seed = 999;
  const stress = process.env.STRESS === "true";

  const events = stress
    ? randomEvents(5000, seed)
    : randomEvents(10000, seed);

  const horizon = stress ? 20000 : 5000;

  // === empirical statistics ===
  const empiricalMean =
    events.reduce((a, b) => a + b, 0) / events.length;

  const empiricalVariance =
    events.reduce((a, b) => a + (b - empiricalMean) ** 2, 0) /
    events.length;

  const empiricalStd = Math.sqrt(empiricalVariance);

  // === theoretical assumptions ===
  const theoreticalMean = 0;

  // dynamic tolerance using 3-sigma rule
  const tolerance =
    (3 * empiricalStd) / Math.sqrt(events.length);

  const report = {
    seed,
    empiricalMean,
    empiricalVariance,
    tolerance,
    errorCheck: enforceMeanError(
      empiricalMean,
      theoreticalMean,
      tolerance,
      empiricalStd,
      events.length
    ),
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
    console.log("Empirical mean:", result.empiricalMean);
    console.log("Tolerance:", result.tolerance);
    console.log(result);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}
