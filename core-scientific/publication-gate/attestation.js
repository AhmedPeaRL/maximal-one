import fs from "fs";
import crypto from "crypto";

const reportPath = new URL("./report.json", import.meta.url);
const attestationPath = new URL("./attestation.json", import.meta.url);

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

export function generateAttestation() {

  if (!fs.existsSync(reportPath)) {
    throw new Error("Report not found");
  }

  const report = JSON.parse(fs.readFileSync(reportPath));

  const attestationPayload = {
    commit: process.env.GITHUB_SHA || "local",
    protocolVersion: report.protocolVersion,
    scientificHash: report.scientificHash,
    compositeSeal: report.compositeSeal,
    deterministicArtifactHash: report.deterministicArtifactHash
  };

  const attestationHash = computeHash(
    stableStringify(attestationPayload)
  );

  const finalAttestation = {
    ...attestationPayload,
    attestationHash
  };

  fs.writeFileSync(
    attestationPath,
    JSON.stringify(finalAttestation, null, 2)
  );

  console.log("Attestation hash:", attestationHash);
}
