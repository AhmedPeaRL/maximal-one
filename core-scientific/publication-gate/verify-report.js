import fs from "fs";
import crypto from "crypto";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function stable(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
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

function computeHash(payload) {
  return crypto.createHash("sha256").update(payload).digest("hex");
}

function verify() {

  const reportPath = new URL("./report.json", import.meta.url);
  const attestationPath = new URL("./attestation.json", import.meta.url);

  if (!fs.existsSync(reportPath)) {
    throw new Error("Report file not found");
  }

  const report = JSON.parse(fs.readFileSync(reportPath));

  const { reportSelfHash, ...rest } = report;

  const recomputedReportHash = computeHash(stableStringify(rest));

  if (recomputedReportHash !== reportSelfHash) {
    throw new Error("Report integrity mismatch");
  }

  if (fs.existsSync(attestationPath)) {

    const attestation = JSON.parse(fs.readFileSync(attestationPath));

    const recomputedAttestation = sha256(stable({
      scientificHash: attestation.scientificHash,
      compositeSeal: attestation.compositeSeal,
      deterministicArtifactHash: attestation.deterministicArtifactHash
    }));

    if (recomputedAttestation !== attestation.attestationHash) {
      throw new Error("Attestation mismatch detected");
    }

    console.log("Attestation integrity verified.");
    console.log("Attestation Hash:", attestation.attestationHash);
  }

  console.log("Report integrity verified.");
  console.log("Deterministic Artifact Hash:", report.deterministicArtifactHash);
  console.log("Scientific Hash:", report.scientificHash);
  console.log("Composite Seal:", report.compositeSeal);
}

verify();
