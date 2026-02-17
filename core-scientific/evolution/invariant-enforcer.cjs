const fs = require("fs");
const path = require("path");

function enforceInvariants() {
  const aggregatedPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "aggregated-report.json"
  );

  if (!fs.existsSync(aggregatedPath)) {
    throw new Error("aggregated-report.json not found.");
  }

  const raw = fs.readFileSync(aggregatedPath, "utf8");

  let reports;
  try {
    reports = JSON.parse(raw);
  } catch (err) {
    throw new Error("Invalid JSON format in aggregated-report.json");
  }

  if (!Array.isArray(reports) || reports.length === 0) {
    throw new Error("Aggregated report is empty or not an array.");
  }

  const normalizedReports = reports.map(r => {
    const hash =
      r.deterministicArtifactHash ||
      r.artifactHash ||
      r.hash ||
      null;

    return {
      region: r.region || "unknown",
      hash
    };
  });

  const validReports = normalizedReports.filter(
    r =>
      typeof r.region === "string" &&
      r.region.length > 0 &&
      typeof r.hash === "string" &&
      r.hash.length === 64
  );

  if (validReports.length === 0) {
    console.error("Aggregated structure received:");
    console.error(JSON.stringify(reports, null, 2));
    throw new Error(
      "No valid reports with region and valid 64-char hash."
    );
  }

  const uniqueHashes = [
    ...new Set(validReports.map(r => r.hash))
  ];

  if (uniqueHashes.length !== 1) {
    throw new Error(
      "Deterministic invariant violated: multiple artifact hashes detected."
    );
  }

  console.log("Invariant enforcement passed.");
  console.log("Consensus hash:", uniqueHashes[0]);

  return uniqueHashes[0];
}

module.exports = { enforceInvariants };
