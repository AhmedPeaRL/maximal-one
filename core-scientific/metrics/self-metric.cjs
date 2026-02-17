const fs = require("fs");
const path = require("path");

function generateSelfMetric(data) {
  const metricPath = path.join(
    __dirname,
    "..",
    "evolution",
    "evolution-metric.json"
  );

  const metric = {
    timestamp: new Date().toISOString(),
    entries: data.entries,
    stateHash: data.stateHash,
    consensusHash: data.consensusHash
  };

  fs.writeFileSync(metricPath, JSON.stringify(metric, null, 2));

  console.log("Self-metric updated.");
}

module.exports = { generateSelfMetric };
