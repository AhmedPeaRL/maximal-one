import fs from "fs";
import crypto from "crypto";

const reportPath = process.argv[2] || "./core-scientific/publication-gate/report.json";
const canonicalPath = "./core-scientific/publication-gate/canonical.json";
const protocolLockPath = "./core-scientific/publication-gate/protocol-lock.json";

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

function computeHash(payload) {
  return crypto.createHash("sha256").update(payload).digest("hex");
}

function assert(condition, message) {
  if (!condition) {
    console.error("AUDIT FAILURE:", message);
    process.exit(1);
  }
}

function audit() {

  assert(fs.existsSync(reportPath), "Report file missing");
  assert(fs.existsSync(canonicalPath), "Canonical missing");
  assert(fs.existsSync(protocolLockPath), "Protocol lock missing");

  const report = JSON.parse(fs.readFileSync(reportPath));
  const canonical = JSON.parse(fs.readFileSync(canonicalPath));
  const protocolLock = JSON.parse(fs.readFileSync(protocolLockPath));

  const { reportSelfHash, ...rest } = report;

  const recomputedSelf = computeHash(stableStringify(rest));
  assert(recomputedSelf === reportSelfHash, "Self-hash mismatch");

  const recomputedArtifact = computeHash(
    stableStringify({
      protocolVersion: report.protocolVersion,
      meanDriftAcrossSeeds: report.meanDriftAcrossSeeds,
      varianceDriftAcrossSeeds: report.varianceDriftAcrossSeeds,
      sensitivityDriftAcrossSeeds: report.sensitivityDriftAcrossSeeds,
      runtimeHash: report.runtimeHash,
      scientificHash: report.scientificHash,
      compositeSeal: report.compositeSeal,
      canonicalHash: report.canonicalHash,
      status: report.status
    })
  );

  assert(recomputedArtifact === report.deterministicArtifactHash, "Deterministic artifact hash mismatch");

  const canonicalHash = computeHash(stableStringify(canonical));
  assert(canonicalHash === protocolLock.canonicalHash, "Canonical hash mismatch with protocol lock");

  console.log("Independent audit: VERIFIED");
  console.log("Scientific Hash:", report.scientificHash);
  console.log("Composite Seal:", report.compositeSeal);
  console.log("Deterministic Artifact Hash:", report.deterministicArtifactHash);
}

audit();
