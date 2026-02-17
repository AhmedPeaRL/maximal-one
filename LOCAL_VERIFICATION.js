const fs = require("fs");
const crypto = require("crypto");
const path = require("path");

function hashFile(filePath) {
  const data = fs.readFileSync(filePath);
  return crypto.createHash("sha256").update(data).digest("hex");
}

function main() {
  const reportPath = path.join(__dirname, "core-scientific", "publication-gate", "report.json");

  if (!fs.existsSync(reportPath)) {
    console.error("report.json not found.");
    process.exit(1);
  }

  const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));

  const scientificHash = report.scientificHash;
  const deterministicArtifactHash = report.deterministicArtifactHash;

  console.log("Scientific Hash:", scientificHash);
  console.log("Deterministic Artifact Hash:", deterministicArtifactHash);

  const manifestPath = path.join(__dirname, "SYSTEM_STATE_MANIFEST.json");

  if (!fs.existsSync(manifestPath)) {
    console.error("SYSTEM_STATE_MANIFEST.json not found.");
    process.exit(1);
  }

  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));

  if (
    manifest.scientific_hash === scientificHash &&
    manifest.deterministic_artifact_hash === deterministicArtifactHash
  ) {
    console.log("Local verification: STATE CONSISTENT");
  } else {
    console.error("Local verification: STATE MISMATCH");
    process.exit(1);
  }
}

main();
