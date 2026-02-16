import fs from "fs";
import crypto from "crypto";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function stable(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

const attestationPath = "./core-scientific/publication-gate/attestation.json";

if (fs.existsSync(attestationPath)) {

  const attestation = JSON.parse(fs.readFileSync(attestationPath));

const reportPath = new URL("./report.json", import.meta.url);

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

function verify() {

  if (!fs.existsSync(reportPath)) {
    throw new Error("Report file not found");
  }

  const report = JSON.parse(fs.readFileSync(reportPath));

  const { reportSelfHash, ...rest } = report;

  const recomputed = sha256(stable({
    scientificHash: attestation.scientificHash,
    compositeSeal: attestation.compositeSeal,
    deterministicArtifactHash: attestation.deterministicArtifactHash
  }));

  if (recomputed !== attestation.attestationHash) {
    console.error("Attestation mismatch detected.");
    process.exit(1);
  }

}

  console.log("Report integrity verified.");
  console.log("Deterministic Artifact Hash:", report.deterministicArtifactHash);
  console.log("Attestation Hash:", report.attestationHash || "N/A");
}

verify();
