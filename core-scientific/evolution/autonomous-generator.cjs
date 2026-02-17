const fs = require("fs");
const path = require("path");

const { enforceEvolutionLock } = require("./evolution-lock.cjs");
const { enforceInvariants } = require("../invariants/invariant-engine.cjs");
const { computeConsensusHash } = require("../consensus/consensus-engine.cjs");
const { generateSelfMetric } = require("../metrics/self-metric.cjs");

function loadAggregatedReport() {
  const reportPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "aggregated-report.json"
  );

  if (!fs.existsSync(reportPath)) {
    throw new Error("Aggregated report not found.");
  }

  return JSON.parse(fs.readFileSync(reportPath, "utf-8"));
}

function computeStateHash(data) {
  const crypto = require("crypto");
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(data))
    .digest("hex");
}

function runEvolution() {
  const aggregated = loadAggregatedReport();

  enforceInvariants(aggregated);

  const consensusHash = computeConsensusHash(aggregated);
  const entries = aggregated.length;

  const stateObject = {
    timestamp: new Date().toISOString(),
    entries,
    consensusHash
  };

  const stateHash = computeStateHash(stateObject);

  console.log("Invariant enforcement passed.");
  console.log("Consensus hash:", consensusHash);
  console.log("Entries:", entries);
  console.log("Structural signature:", stateHash);

  enforceEvolutionLock(stateHash);

  generateSelfMetric({
    entries,
    stateHash,
    consensusHash
  });

  console.log("Autonomous evolution committed.");
}

runEvolution();
