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

const baselinePath = new URL("./baseline.json", import.meta.url);
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
(typeof obj[prop] === "object" || typeof obj[prop] === "function") &&
!Object.isFrozen(obj[prop])
) {
deepFreeze(obj[prop]);
}
});
}
return obj;
}

function computeHash(payload) {
return crypto
.createHash("sha256")
.update(payload)
.digest("hex");
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

assert(
recomputed === reportSelfHash,
"Report self-hash verification failed"
);
}

async function publicationGate() {

verifyExistingReport();

assert(
protocolLock.protocolVersion === SCIENTIFIC_PROTOCOL_VERSION,
"Protocol version mismatch with protocol-lock"
);

assert(
protocolLock.expectedNodeMajor === EXPECTED_NODE_MAJOR,
"Node expectation mismatch with protocol-lock"
);

assert(
protocolLock.quantizationDigits === FIXED_QUANTIZATION_DIGITS,
"Quantization governance mismatch"
);

assert(
protocolLock.structuralEpsilon === STRUCTURAL_EPSILON,
"Structural epsilon governance mismatch"
);

const nodeMajor = parseInt(process.version.split(".")[0].replace("v",""));
assert(
nodeMajor === EXPECTED_NODE_MAJOR,
Node major version mismatch. Expected ${EXPECTED_NODE_MAJOR}
);

assert(
Array.isArray(seedsConfig.seeds) && seedsConfig.seeds.length > 0,
"Invalid seeds configuration"
);

const runtimeSeal = computeRuntimeSeal();
assert(
runtimeSeal && runtimeSeal.runtimeHash,
"Runtime seal invalid"
);

const results = [];

const orderedSeeds = [...seedsConfig.seeds].sort((a, b) => a - b);

for (const seed of orderedSeeds) {

const empirical = runEmpiricalValidation(seed);  
const sensitivity = runSensitivitySuite(seed);  
const bifurcation = runBifurcationScan(seed);  

const relError = empirical.relativeError;  
const variance = empirical.empiricalStd ** 2;  

const chaoticRegions = bifurcation.filter(b => b.lyapunov > 0);  
const stableRegions = bifurcation.filter(b => b.lyapunov < 0);  

const sensitivityMeans = sensitivity.map(s => s.mean);  
const sensitivityDrift = computeDrift(sensitivityMeans);  

assert(relError < protocolLock.relativeErrorThreshold, `Relative error exceeds threshold (seed ${seed})`);  
assert(variance > 0, `Variance zero (seed ${seed})`);  
assert(chaoticRegions.length > 0, `No chaos (seed ${seed})`);  
assert(stableRegions.length > 0, `No stability (seed ${seed})`);  
assert(sensitivityDrift < protocolLock.perSeedSensitivityThreshold, `Sensitivity instability (seed ${seed})`);  

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

const envelope = deepFreeze({
protocolVersion: SCIENTIFIC_PROTOCOL_VERSION,
meanDriftAcrossSeeds: quantize(computeDrift(means)),
varianceDriftAcrossSeeds: quantize(computeDrift(variances)),
sensitivityDriftAcrossSeeds: quantize(computeDrift(drifts))
});

assert(envelope.meanDriftAcrossSeeds < protocolLock.seedMeanDriftThreshold, "Mean unstable across seeds");
assert(envelope.varianceDriftAcrossSeeds < protocolLock.seedVarianceDriftThreshold, "Variance unstable across seeds");
assert(envelope.sensitivityDriftAcrossSeeds < protocolLock.seedSensitivityDriftThreshold, "Sensitivity unstable across seeds");

const epsilon = STRUCTURAL_EPSILON;

const totalDrift =
envelope.meanDriftAcrossSeeds +
envelope.varianceDriftAcrossSeeds +
epsilon;

const invariant =
envelope.meanDriftAcrossSeeds / totalDrift;

// Structural invariant must remain bounded
assert(
invariant >= protocolLock.invariantMin &&
invariant <= protocolLock.invariantMax,
Structural invariant violation: ${invariant}
);

const scientificHash = computeScientificHash(envelope);

// Canonical initialization
if (!fs.existsSync(canonicalPath)) {
const canonicalPayload = {
protocolVersion: SCIENTIFIC_PROTOCOL_VERSION,
scientificHash
};
fs.writeFileSync(canonicalPath, JSON.stringify(canonicalPayload, null, 2));
}

// Canonical governance
const canonical = JSON.parse(fs.readFileSync(canonicalPath));

assert(
canonical.protocolVersion === SCIENTIFIC_PROTOCOL_VERSION,
"Canonical protocol version mismatch"
);

if (canonical.scientificHash !== scientificHash) {

if (!process.env.GITHUB_SHA) {  
  throw new Error("Scientific identity drift detected (no commit context)");  
}  

const upgradePolicy = JSON.parse(fs.readFileSync(canonicalUpgradePath));  

assert(upgradePolicy.allowUpgrade === true, "Scientific identity drift detected (upgrade not authorized)");  
assert(upgradePolicy.requiredCommit === process.env.GITHUB_SHA, "Upgrade commit mismatch");  
assert(upgradePolicy.upgradeProtocolVersion === SCIENTIFIC_PROTOCOL_VERSION, "Upgrade protocol version mismatch");  

fs.writeFileSync(  
  canonicalPath,  
  JSON.stringify(  
    { protocolVersion: SCIENTIFIC_PROTOCOL_VERSION, scientificHash },  
    null,  
    2  
  )  
);

}

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
status: "MULTI_SEED_VERIFIED"
};

const executionContext = {
commit: process.env.GITHUB_SHA || "local",
environmentClass: runtimeSeal.environmentClass
};

const deterministicArtifactHash = computeHash(
stableStringify(identityPayload)
);

const finalTimestamp = new Date().toISOString();

const finalReportPayload = {
timestamp: finalTimestamp,
...identityPayload,
...executionContext,
deterministicArtifactHash
};

const reportSelfHash = computeHash(
stableStringify(finalReportPayload)
);

const finalReport = {
...finalReportPayload,
reportSelfHash
};

const canonicalReport = JSON.parse(
stableStringify(finalReport)
);

fs.writeFileSync(
reportPath,
JSON.stringify(canonicalReport, null, 2)
);

console.log("Scientific hash:", scientificHash);
console.log("Composite seal:", compositeSeal);
console.log("Multi-Seed Gate: PASSED");
}

publicationGate();
