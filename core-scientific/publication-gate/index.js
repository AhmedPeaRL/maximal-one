import { computeRuntimeSeal } from "./runtime-seal.js";
import fs from "fs";
import crypto from "crypto";
import { runEmpiricalValidation } from "../empirical/empirical-test.js";
import { runSensitivitySuite } from "../sensitivity/sensitivity-test.js";
import { runBifurcationScan } from "../nonlinear/bifurcation-test.js";

const SCIENTIFIC_PROTOCOL_VERSION = "2.0.0";
const EXPECTED_NODE_MAJOR = 18;

const baselinePath = new URL("./baseline.json", import.meta.url);

const seedsConfig = JSON.parse(
  fs.readFileSync(new URL("./seeds.json", import.meta.url))
);

function loadBaseline() {
  return JSON.parse(fs.readFileSync(baselinePath));
}

function saveBaseline(data) {
  fs.writeFileSync(
    baselinePath,
    JSON.stringify(data, null, 2)
  );
}

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

async function publicationGate() {

  const nodeMajor = parseInt(process.version.split(".")[0].replace("v",""));
  assert(
    nodeMajor === EXPECTED_NODE_MAJOR,
    `Node major version mismatch. Expected ${EXPECTED_NODE_MAJOR}`
  );

  const runtimeSeal = computeRuntimeSeal();

  console.log("---- MULTI-SEED DIAGNOSTICS ----");

  const seeds = seedsConfig.seeds;
  const results = [];

  for (const seed of seeds) {

    const empirical = runEmpiricalValidation(seed);
    const sensitivity = runSensitivitySuite(seed);
    const bifurcation = runBifurcationScan(seed);

    const relError = empirical.relativeError;
    const variance = empirical.empiricalStd ** 2;

    const chaoticRegions = bifurcation.filter(b => b.lyapunov > 0);
    const stableRegions = bifurcation.filter(b => b.lyapunov < 0);

    const sensitivityMeans = sensitivity.map(s => s.mean);
    const sensitivityDrift = computeDrift(sensitivityMeans);

    assert(relError < 0.01, `Relative error exceeds 1% (seed ${seed})`);
    assert(variance > 0, `Variance zero (seed ${seed})`);
    assert(chaoticRegions.length > 0, `No chaos (seed ${seed})`);
    assert(stableRegions.length > 0, `No stability (seed ${seed})`);
    assert(sensitivityDrift < 0.05, `Sensitivity instability (seed ${seed})`);

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

  const envelope = {
    protocolVersion: SCIENTIFIC_PROTOCOL_VERSION,
    meanDriftAcrossSeeds: quantize(computeDrift(means)),
    varianceDriftAcrossSeeds: quantize(computeDrift(variances)),
    sensitivityDriftAcrossSeeds: quantize(computeDrift(drifts))
  };

  assert(envelope.meanDriftAcrossSeeds < 0.01, "Mean unstable across seeds");
  assert(envelope.varianceDriftAcrossSeeds < 0.01, "Variance unstable across seeds");
  assert(envelope.sensitivityDriftAcrossSeeds < 0.01, "Sensitivity unstable across seeds");

  let baseline = loadBaseline();

  if (baseline.initialize === true) {
    saveBaseline(envelope);
    console.log("Baseline initialized from current envelope.");
    baseline = envelope;
  }

  if (baseline.protocolVersion === envelope.protocolVersion) {

    const driftTolerance = 1e-6;

    assert(
      Math.abs(envelope.meanDriftAcrossSeeds - baseline.meanDriftAcrossSeeds) < driftTolerance,
      "Mean drift regression detected"
    );

    assert(
      Math.abs(envelope.varianceDriftAcrossSeeds - baseline.varianceDriftAcrossSeeds) < driftTolerance,
      "Variance drift regression detected"
    );

    assert(
      Math.abs(envelope.sensitivityDriftAcrossSeeds - baseline.sensitivityDriftAcrossSeeds) < driftTolerance,
      "Sensitivity drift regression detected"
    );
  }

  const scientificHash = computeScientificHash(envelope);

  const compositeSeal = computeScientificHash({
    scientificHash,
    runtimeHash: runtimeSeal.runtimeHash
  });

  const finalReport = {
    timestamp: new Date().toISOString(),
    commit: process.env.GITHUB_SHA || "local",
    ...envelope,
    runtimeHash: runtimeSeal.runtimeHash,
    runtimeFingerprint: runtimeSeal.fingerprint,
    scientificHash,
    compositeSeal,
    status: "MULTI_SEED_VERIFIED"
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
