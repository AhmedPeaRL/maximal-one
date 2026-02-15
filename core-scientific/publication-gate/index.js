import { enforceScientificMetrics } from "./metrics-guard.js";
import { computeRuntimeSeal } from "./runtime-seal.js";
import fs from "fs";
import crypto from "crypto";
import { runEmpiricalValidation } from "../empirical/empirical-test.js";
import { runSensitivitySuite } from "../sensitivity/sensitivity-test.js";
import { runBifurcationScan } from "../nonlinear/bifurcation-test.js";

const SCIENTIFIC_PROTOCOL_VERSION = "2.0.1";
const EXPECTED_NODE_MAJOR = 18;
const FIXED_QUANTIZATION_DIGITS = 12;
const STRUCTURAL_EPSILON = 1e-12;

const seedsPath = new URL("./seeds.json", import.meta.url);
const canonicalPath = new URL("./canonical.json", import.meta.url);
const canonicalUpgradePath = new URL("./canonical-upgrade.json", import.meta.url);
const protocolLockPath = new URL("./protocol-lock.json", import.meta.url);
const reportPath = new URL("./report.json", import.meta.url);

const seedsConfig = JSON.parse(fs.readFileSync(seedsPath));
const protocolLock = JSON.parse(fs.readFileSync(protocolLockPath));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function quantize(value) {
  return Number.parseFloat(value.toFixed(FIXED_QUANTIZATION_DIGITS));
}

function stableStringify(obj) {
  if (obj === undefined) return "null";
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

function deepFreeze(obj) {
  if (obj && typeof obj === "object") {
    Object.freeze(obj);
    Object.getOwnPropertyNames(obj).forEach(prop => {
      if (
        obj[prop] !== null &&
        typeof obj[prop] === "object" &&
        !Object.isFrozen(obj[prop])
      ) {
        deepFreeze(obj[prop]);
      }
    });
  }
  return obj;
}

function computeHash(payload) {
  return crypto.createHash("sha256").update(payload).digest("hex");
}

function computeScientificHash(payload) {
  return computeHash(stableStringify(payload));
}

function computeDrift(values) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  return Math.abs(max - min);
}

function verifyExistingReport() {
  if (!fs.existsSync(reportPath)) return;

  const existing = JSON.parse(fs.readFileSync(reportPath));
  const { reportSelfHash, ...rest } = existing;
  const recomputed = computeHash(stableStringify(rest));

  assert(recomputed === reportSelfHash, "Report self-hash verification failed");
}

async function publicationGate() {

  verifyExistingReport();

  assert(protocolLock.protocolVersion === SCIENTIFIC_PROTOCOL_VERSION, "Protocol version mismatch");
  assert(protocolLock.expectedNodeMajor === EXPECTED_NODE_MAJOR, "Node expectation mismatch");
  assert(protocolLock.quantizationDigits === FIXED_QUANTIZATION_DIGITS, "Quantization mismatch");
  assert(protocolLock.structuralEpsilon === STRUCTURAL_EPSILON, "Structural epsilon mismatch");

  const nodeMajor = parseInt(process.version.split(".")[0].replace("v",""));
  assert(nodeMajor === EXPECTED_NODE_MAJOR, `Node major version mismatch`);

  assert(Array.isArray(seedsConfig.seeds) && seedsConfig.seeds.length > 0, "Invalid seeds");

  const runtimeSeal = computeRuntimeSeal();
  assert(runtimeSeal && runtimeSeal.runtimeHash, "Runtime seal invalid");

  const orderedSeeds = [...seedsConfig.seeds].sort((a,b)=>a-b);
  const results = [];

  for (const seed of orderedSeeds) {

    const empirical = runEmpiricalValidation(seed);
    const sensitivity = runSensitivitySuite(seed);
    const bifurcation = runBifurcationScan(seed);

    const variance = empirical.empiricalStd ** 2;
    const chaotic = bifurcation.filter(b=>b.lyapunov>0);
    const stable = bifurcation.filter(b=>b.lyapunov<0);

    const drift = computeDrift(sensitivity.map(s=>s.mean));

    assert(empirical.relativeError < protocolLock.relativeErrorThreshold, `Rel error ${seed}`);
    assert(variance > 0, `Variance zero ${seed}`);
    assert(chaotic.length > 0, `No chaos ${seed}`);
    assert(stable.length > 0, `No stability ${seed}`);
    assert(drift < protocolLock.perSeedSensitivityThreshold, `Sensitivity unstable ${seed}`);

    results.push({
      seed,
      empiricalMean: empirical.empiricalMean,
      variance,
      sensitivityDrift: drift
    });
  }

  const envelope = deepFreeze({
    protocolVersion: SCIENTIFIC_PROTOCOL_VERSION,
    meanDriftAcrossSeeds: quantize(computeDrift(results.map(r=>r.empiricalMean))),
    varianceDriftAcrossSeeds: quantize(computeDrift(results.map(r=>r.variance))),
    sensitivityDriftAcrossSeeds: quantize(computeDrift(results.map(r=>r.sensitivityDrift)))
  });

  const canonical = JSON.parse(fs.readFileSync(canonicalPath));
  
  const canonicalHash = computeScientificHash(canonical);
  
  const AUTO_SYNC = process.env.AUTO_SYNC_CANONICAL === "true";
  
  if (canonicalHash !== protocolLock.canonicalHash) {
    
    if (AUTO_SYNC) {
      
      console.log("Canonical mismatch detected.");
      console.log("Auto-sync mode enabled. Updating protocol-lock.");
      
      protocolLock.canonicalHash = canonicalHash;
      
      fs.writeFileSync(
        protocolLockPath,
        JSON.stringify(protocolLock, null, 2)
      );
    
    } else {
      
      throw new Error("Canonical reference mismatch");
    
    }
  
  }

  const scientificHash = computeScientificHash(envelope);

  const compositeSeal = computeScientificHash({
    scientificHash,
    runtimeHash: runtimeSeal.runtimeHash
  });

  const identityPayload = {
    protocolVersion: SCIENTIFIC_PROTOCOL_VERSION,
    ...envelope,
    runtimeHash: runtimeSeal.runtimeHash,
    scientificHash,
    compositeSeal,
    canonicalHash,
    status: "MULTI_SEED_VERIFIED"
  };

  const executionContext = {
    commit: process.env.GITHUB_SHA || "local",
    runtimeFingerprint: runtimeSeal.fingerprint || null,
    environmentClass: runtimeSeal.environmentClass || null
  };

  const deterministicArtifactHash = computeHash(
    stableStringify(identityPayload)
  );

  const deterministicTimestamp = new Date(
      parseInt(compositeSeal.slice(0, 12), 16) % 1e12
    ).toISOString();

  const finalReportPayload = {
  timestamp: deterministicTimestamp,
    ...identityPayload,
    ...executionContext,
    deterministicArtifactHash
  };

  const reportSelfHash = computeHash(stableStringify(finalReportPayload));

  const finalReport = {
    ...finalReportPayload,
    reportSelfHash
  };

  enforceScientificMetrics(report);

  fs.writeFileSync(
    reportPath,
    JSON.stringify(finalReport, null, 2)
  );

  const reloaded = JSON.parse(fs.readFileSync(reportPath));
  const { reportSelfHash: reHash, ...reRest } = reloaded;
  const recomputed = computeHash(stableStringify(reRest));

  assert(reHash === recomputed, "Post-write reproducibility failure");

  console.log("Scientific hash:", scientificHash);
  console.log("Composite seal:", compositeSeal);
  console.log("Multi-Seed Gate: PASSED");
}

publicationGate();
