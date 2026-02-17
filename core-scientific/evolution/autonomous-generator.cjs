const fs = require("fs");
const path = require("path");

const { enforceInvariants } = require("../invariants/invariant-engine.cjs");
const { computeConsensusHash } = require("../consensus/consensus-engine.cjs");
const { generateSelfMetric } = require("../metrics/self-metric.cjs");
const { enforceEvolutionLock } = require("./evolution-lock.cjs");

function collectReports() {
  const reportsDir = path.join(__dirname, "..", "..", "reports");

  if (!fs.existsSync(reportsDir)) {
    throw new Error("Reports directory not found.");
  }

  const regionFolders = fs
    .readdirSync(reportsDir)
    .filter((f) =>
      fs.statSync(path.join(reportsDir, f)).isDirectory()
    );

  const aggregated = [];

  regionFolders.forEach((regionFolder) => {
    const reportPath = path.join(
      reportsDir,
      regionFolder,
      "report.json"
    );

    if (!fs.existsSync(reportPath)) return;

    const content = JSON.parse(
      fs.readFileSync(reportPath, "utf-8")
    );

    // لو التقرير array
    const entries = Array.isArray(content) ? content : [content];

    entries.forEach((entry) => {
      if (!entry.deterministicArtifactHash) {
        throw new Error(
          `Missing deterministicArtifactHash in ${regionFolder}`
        );
      }

      aggregated.push({
        region: regionFolder.replace("report-", ""),
        deterministicArtifactHash:
          entry.deterministicArtifactHash
      });
    });
  });

  return aggregated.sort((a, b) =>
    a.region.localeCompare(b.region)
  );
}

function runEvolution() {
  const aggregated = collectReports();

  enforceInvariants(aggregated);

  const consensusHash =
    computeConsensusHash(aggregated);

  const stateHash = require("crypto")
    .createHash("sha256")
    .update(JSON.stringify(aggregated))
    .digest("hex");

  console.log("Consensus hash:", consensusHash);
  console.log("State hash:", stateHash);

  enforceEvolutionLock(stateHash);

  generateSelfMetric({
    entries: aggregated.length,
    stateHash,
    consensusHash
  });

  console.log("Autonomous evolution committed.");
}

runEvolution();
