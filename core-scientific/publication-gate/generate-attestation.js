import fs from "fs";
import crypto from "crypto";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function stable(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

function main() {

  const reportPath = "./core-scientific/publication-gate/report.json";

  if (!fs.existsSync(reportPath)) {
    console.error("Report not found.");
    process.exit(1);
  }

  const report = JSON.parse(fs.readFileSync(reportPath));

  const attestation = {
    scientificHash: report.scientificHash,
    compositeSeal: report.compositeSeal,
    deterministicArtifactHash: report.deterministicArtifactHash
  };

  const attestationHash = sha256(stable(attestation));

  const output = {
    ...attestation,
    attestationHash
  };

  fs.writeFileSync(
    "./core-scientific/publication-gate/attestation.json",
    JSON.stringify(output, null, 2)
  );

  console.log("Attestation Hash Generated:");
  console.log(attestationHash);
}

main();
