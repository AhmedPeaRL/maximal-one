import { computeRuntimeSeal } from "./runtime-seal.js";
import fs from "fs";
import crypto from "crypto";
import { runEmpiricalValidation } from "../empirical/empirical-test.js";
import { runSensitivitySuite } from "../sensitivity/sensitivity-test.js";
import { runBifurcationScan } from "../nonlinear/bifurcation-test.js";

const SCIENTIFIC_PROTOCOL_VERSION = "2.0.1";
const EXPECTED_NODE_MAJOR = 18;

const baselinePath = new URL("./baseline.json", import.meta.url);
const seedsPath = new URL("./seeds.json", import.meta.url);
const canonicalPath = new URL("./canonical.json", import.meta.url);
const protocolLockPath = new URL("./protocol-lock.json", import.meta.url);

const seedsConfig = JSON.parse(fs.readFileSync(seedsPath));
const protocolLock = JSON.parse(fs.readFileSync(protocolLockPath));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function quantize(value, digits = 12) {
  return Number.parseFloat(value.toFixed(digits));
}

function stableStringify(obj) {
  if (obj === null || typeof obj !== "object") {
    return JSON.stringify(obj);
  }

  if (Array.isArray(obj)) {
    return "[" + obj.map(stableStringify).join(",") + "]";
  }

  const keys = Object.keys(obj).sort();
  return (
    "{" +
    keys.map(k => JSON.stringify(k) + ":" + stableStringify(obj[k])).join(",") +
    "}"
  );
}

function computeScientificHash(payload) {
  return crypto
    .createHash("sha256")
    .update(stableStringify(payload))
    .digest("hex");
}

function computeDrift(values) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  return Math.abs(max - min);
}

function loadBaseline() {
  if (!fs.existsSync(baselinePath)) {
    return { initialize: true };
  }
  return JSON.parse(fs.readFileSync(baselinePath));
}

function saveBaseline(data) {
  fs.writeFileSync(baselinePath, JSON.stringify(data, null, 2));
}

async function publicationGate() {

  assert(
    protocolLock.protocolVersion === SCIENTIFIC_PROTOCOL_VERSION,
    "Protocol version mismatch with protocol-lock"
  );

  assert(
    protocolLock.expectedNodeMajor === EXPECTED_NODE_MAJOR,
    "Node expectation mismatch with protocol-lock"
  );

  const nodeMajor = parseInt(process.version.split(".")[0].replace("v",""));
  assert(
    nodeMajor === EXPECTED_NODE_MAJOR,
    `Node major version mismatch. Expected ${EXPECTED_NODE_MAJOR}`
  );

  assert(
    Array.isArray(seedsConfig.seeds) && seedsConfig.seeds.length > 0,
    "Invalid seeds configuration"
  );

  const runtimeSeal = computeRuntimeSeal();

  console.log("---- MULTI-SEED DIAGNOSTICS ----");

  const results = [];

  for (const seed of seedsConfig.seeds) {

    const empirical = runEmpiricalValidation(seed);
    const sensitivity = runSensitivitySuite(seed);
    const bifurcation = runBifurcationScan(seed);

    const relError = empirical.relativeError;
    const variance = empirical.empiricalStd ** 2;

    const chaoticRegions = bifurcation.filter(b => b.lyapunov > 0);
    const stableRegions = bifurcation.filter(b => b.lyapunov < 0);

    const sensitivityMeans = sensitivity.map(s => s.mean);
    const sensitivityDrift = computeDrift(sensitivityMeans);

    assert(
      relError < protocolLock.relativeErrorThreshold,
      `Relative error exceeds threshold (seed ${seed})`
    );

    assert(variance > 0, `Variance zero (seed ${seed})`);
    assert(chaoticRegions.length > 0, `No chaos (seed ${seed})`);
    assert(stableRegions.length > 0, `No stability (seed ${seed})`);

    assert(
      sensitivityDrift < protocolLock.perSeedSensitivityThreshold,
      `Sensitivity instability (seed ${seed})`
    );

    results.push({
      seed,
      empiricalMean: empirical.empiricalMean,
      variance,
      sensitivityDrift
    });
  }

  const means = results.map(r => r.empiricalMean);
  const variances = results.map(r => r.variance);
  const drifts = results.map(r => r.sensitivityDrift);

  const envelope = Object.freeze({
    protocolVersion: SCIENTIFIC_PROTOCOL_VERSION,
    meanDriftAcrossSeeds: quantize(computeDrift(means)),
    varianceDriftAcrossSeeds: quantize(computeDrift(variances)),
    sensitivityDriftAcrossSeeds: quantize(computeDrift(drifts))
  });

  assert(
    envelope.meanDriftAcrossSeeds < protocolLock.seedMeanDriftThreshold,
    "Mean unstable across seeds"
  );

  assert(
    envelope.varianceDriftAcrossSeeds < protocolLock.seedVarianceDriftThreshold,
    "Variance unstable across seeds"
  );

  assert(
    envelope.sensitivityDriftAcrossSeeds < protocolLock.seedSensitivityDriftThreshold,
    "Sensitivity unstable across seeds"
  );

  let baseline = loadBaseline();

  if (baseline.initialize === true) {
    saveBaseline(envelope);
    console.log("Baseline initialized from current envelope.");
    baseline = envelope;
  }

  if (baseline.protocolVersion === envelope.protocolVersion) {

    assert(
      Math.abs(envelope.meanDriftAcrossSeeds - baseline.meanDriftAcrossSeeds)
        < protocolLock.regressionTolerance,
      "Mean drift regression detected"
    );

    assert(
      Math.abs(envelope.varianceDriftAcrossSeeds - baseline.varianceDriftAcrossSeeds)
        < protocolLock.regressionTolerance,
      "Variance drift regression detected"
    );

    assert(
      Math.abs(envelope.sensitivityDriftAcrossSeeds - baseline.sensitivityDriftAcrossSeeds)
        < protocolLock.regressionTolerance,
      "Sensitivity drift regression detected"
    );
  }

  const scientificHash = computeScientificHash(envelope);

  if (fs.existsSync(canonicalPath)) {
    const canonical = JSON.parse(fs.readFileSync(canonicalPath));

    if (canonical.protocolVersion === SCIENTIFIC_PROTOCOL_VERSION) {
      assert(
        canonical.scientificHash === scientificHash,
        "Scientific identity drift detected"
      );
    }
  }

  const compositeSeal = computeScientificHash({
    scientificHash,
    runtimeHash: runtimeSeal.runtimeHash
  });

  const preliminaryReport = {
  timestamp: new Date().toISOString(),
  commit: process.env.GITHUB_SHA || "local",
  ...envelope,
  runtimeHash: runtimeSeal.runtimeHash,
  runtimeFingerprint: runtimeSeal.fingerprint,
  scientificHash,
  compositeSeal,
  status: "MULTI_SEED_VERIFIED"
};

const reportString = stableStringify(preliminaryReport);

const reportHash = crypto
  .createHash("sha256")
  .update(reportString)
  .digest("hex");

const finalReport = {
  ...preliminaryReport,
  reportSelfHash: reportHash
};

fs.writeFileSync(
  "./core-scientific/publication-gate/report.json",
  JSON.stringify(finalReport, null, 2)
);

  console.log("Scientific hash:", scientificHash);
  console.log("Composite seal:", compositeSeal);
  console.log("Multi-Seed Gate: PASSED");
}

publicationGate();
