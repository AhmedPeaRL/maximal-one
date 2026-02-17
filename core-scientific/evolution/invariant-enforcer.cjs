const fs = require("fs");
const path = require("path");

function enforceInvariants() {
  const publicationGatePath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "aggregated-report.json"
  );

  if (!fs.existsSync(publicationGatePath)) {
    throw new Error(`Aggregated report not found at ${publicationGatePath}`);
  }

  const raw = fs.readFileSync(publicationGatePath, "utf-8");

  let reports;
  try {
    reports = JSON.parse(raw);
  } catch {
    throw new Error("Aggregated report is not valid JSON.");
  }

  if (!Array.isArray(reports)) {
    throw new Error("Aggregated report must be an array.");
  }

  if (reports.length === 0) {
    throw new Error("Aggregated report is empty.");
  }

  const normalized = reports
    .filter(r => r && typeof r === "object")
    .map(r => ({
      region: r.region,
      deterministicArtifactHash: r.deterministicArtifactHash
    }))
    .filter(r => r.region && r.deterministicArtifactHash);

  if (normalized.length === 0) {
    throw new Error("No valid reports with region and deterministicArtifactHash.");
  }

  const uniqueHashes = new Set(
    normalized.map(r => r.deterministicArtifactHash)
  );

  if (uniqueHashes.size !== 1) {
    throw new Error("Deterministic hash mismatch across regions.");
  }

  return {
    consensusHash: [...uniqueHashes][0],
    regions: normalized.map(r => r.region)
  };
}

module.exports = { enforceInvariants };
