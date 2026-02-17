const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function loadCurrentState() {
  const reportPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "aggregated-report.json"
  );

  if (!fs.existsSync(reportPath)) {
    throw new Error(
      "aggregated-report.json not found. Cannot load current state."
    );
  }

  const raw = fs.readFileSync(reportPath, "utf-8");
  const data = JSON.parse(raw);

  if (!Array.isArray(data)) {
    throw new Error("Aggregated report must be an array.");
  }

  return data;
}

function computeStateHash(state) {
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(state))
    .digest("hex");
}

function executeTransition() {
  const state = loadCurrentState();
  const hash = computeStateHash(state);

  const transition = {
    timestamp: new Date().toISOString(),
    entries: state.length,
    stateHash: hash
  };

  const outputPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "state-transition.json"
  );

  fs.writeFileSync(outputPath, JSON.stringify(transition, null, 2));

  console.log("State transition executed.");
  console.log("State hash:", hash);

  return transition;
}

module.exports = { executeTransition };
