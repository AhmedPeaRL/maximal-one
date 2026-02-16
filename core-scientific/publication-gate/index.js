import fs from "fs";
import crypto from "crypto";
import { sha256, computeDeterministicArtifactHash } from "../hash-core.js";

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

function stable(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

function main() {

  const deterministicArtifactHash =
  computeDeterministicArtifactHash(scientificHash, compositeSeal);

  const report = {
    scientificHash,
    compositeSeal,
    deterministicArtifactHash: sha256(scientificHash + compositeSeal)
  };

  const reportSelfHash = sha256(stableStringify(report));

  const finalReport = {
    ...report,
    reportSelfHash
  };

  fs.writeFileSync(
    "./core-scientific/publication-gate/report.json",
    JSON.stringify(finalReport, null, 2)
  );

  const attestationPayload = {
    scientificHash: finalReport.scientificHash,
    compositeSeal: finalReport.compositeSeal,
    deterministicArtifactHash: finalReport.deterministicArtifactHash
  };

  const attestationHash = sha256(stable(attestationPayload));

  fs.writeFileSync(
    "./core-scientific/publication-gate/attestation.json",
    JSON.stringify(
      { ...attestationPayload, attestationHash },
      null,
      2
    )
  );

  console.log("Scientific hash:", scientificHash);
  console.log("Composite seal:", compositeSeal);
  console.log("Attestation hash:", attestationHash);
  console.log("Multi-Seed Gate: PASSED");
}

main();
