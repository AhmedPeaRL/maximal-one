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
    throw new Error(
      `Aggregated report not found at ${publicationGatePath}`
    );
  }

  const raw = fs.readFileSync(publicationGatePath, "utf-8");

  let reports;

  try {
    reports = JSON.parse(raw);
  } catch (err) {
    throw new Error("Aggregated report is not valid JSON.");
  }

  if (!Array.isArray(reports) || reports.length === 0) {
    throw new Error("Aggregated report is empty or malformed.");
  }

  for (const report of reports) {
    if (!report.region) {
      throw new Error("Report missing region field.");
    }

    if (!report.deterministicArtifactHash) {
      throw new Error(
        `Report from ${report.region} missing deterministicArtifactHash`
      );
    }
  }

  const uniqueHashes = new Set(
    reports.map(r => r.deterministicArtifactHash)
  );

  if (uniqueHashes.size !== 1) {
    throw new Error(
      "Deterministic hash mismatch across regions."
    );
  }

  return {
    consensusHash: [...uniqueHashes][0],
    regions: reports.map(r => r.region)
  };
}

module.exports = { enforceInvariants };
