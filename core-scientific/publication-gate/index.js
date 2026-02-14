import fs from "fs";
import crypto from "crypto";
import { runEmpiricalValidation } from "../empirical/empirical-test.js";
import { runSensitivitySuite } from "../sensitivity/sensitivity-test.js";
import { runBifurcationScan } from "../nonlinear/bifurcation-test.js";

const baseline = JSON.parse(
  fs.readFileSync(new URL("./baseline.json", import.meta.url))
);

function isFiniteArray(arr) {
  return arr.every(v => Number.isFinite(v));
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function computeDrift(values) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  return Math.abs(max - min);
}

function computeIntegrityHash(payload) {
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(payload))
    .digest("hex");
}

async function publicationGate() {

  console.log("---- DIAGNOSTICS ----");

  const empirical = runEmpiricalValidation();
  const sensitivity = runSensitivitySuite();
  const bifurcation = runBifurcationScan();

  const relError = empirical.relativeError;
  const variance = empirical.empiricalStd ** 2;

  const chaoticRegions = bifurcation.filter(b => b.lyapunov > 0);
  const stableRegions = bifurcation.filter(b => b.lyapunov < 0);

  const sensitivityMeans = sensitivity.map(s => s.mean);
  const sensitivityDrift = computeDrift(sensitivityMeans);

  const meanDiff = Math.abs(empirical.empiricalMean - baseline.expectedMean);
  const varianceDiff = Math.abs(variance - baseline.expectedVariance);
  const driftDiff = Math.abs(
    sensitivityDrift - baseline.expectedSensitivityDrift
  );

  console.log("Empirical Mean:", empirical.empiricalMean);
  console.log("Relative Error:", relError);
  console.log("Variance:", variance);
  console.log("Chaotic regions:", chaoticRegions.length);
  console.log("Stable regions:", stableRegions.length);
  console.log("Sensitivity drift:", sensitivityDrift);

  assert(relError < 0.01, "Relative error exceeds 1%");
  assert(variance > 0, "Variance is zero");
  assert(chaoticRegions.length > 0, "No chaotic regime detected");
  assert(stableRegions.length > 0, "No stable regime detected");
  assert(sensitivityDrift < 0.05, "Sensitivity instability detected");
  assert(isFiniteArray(sensitivityMeans), "Non-finite sensitivity values");
  assert(
    bifurcation.every(b => Number.isFinite(b.lyapunov)),
    "Non-finite Lyapunov values detected"
  );

  assert(meanDiff < 0.003, "Mean regression detected");
  assert(varianceDiff < 0.002, "Variance regression detected");
  assert(driftDiff < 0.001, "Sensitivity regression detected");

  const reportCore = {
    timestamp: new Date().toISOString(),
    commit: process.env.GITHUB_SHA || "local",
    empirical,
    chaoticRegionsCount: chaoticRegions.length,
    stableRegionsCount: stableRegions.length,
    sensitivityDrift,
    integrity: "SELF_CONSISTENT",
    status: "READY_FOR_PUBLICATION"
  };

  const integrityHash = computeIntegrityHash(reportCore);

  const finalReport = {
    ...reportCore,
    integrityHash
  };

  fs.writeFileSync(
    "./core-scientific/publication-gate/report.json",
    JSON.stringify(finalReport, null, 2)
  );

  console.log("Integrity hash:", integrityHash);
  console.log("Publication Gate: PASSED");
}

publicationGate();
