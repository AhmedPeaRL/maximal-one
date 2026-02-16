import fs from "fs";
import crypto from "crypto";

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

  const recomputed = computeHash(stableStringify(rest));

  if (recomputed !== reportSelfHash) {
    throw new Error("Report integrity verification failed");
  }

  console.log("Report integrity verified.");
  console.log("Deterministic Artifact Hash:", report.deterministicArtifactHash);
  console.log("Attestation Hash:", report.attestationHash || "N/A");
}

verify();
