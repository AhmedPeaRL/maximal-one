const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const REPORT_PATH = path.join(
  __dirname,
  "..",
  "publication-gate",
  "report.json"
);

function loadReport() {
  if (!fs.existsSync(REPORT_PATH)) {
    console.log("No report found. Evolution skipped.");
    process.exit(0);
  }

  const raw = fs.readFileSync(REPORT_PATH, "utf-8");
  return JSON.parse(raw);
}

function computeEvolutionHash(report) {
  const stable = JSON.stringify(report, Object.keys(report).sort());
  return crypto.createHash("sha256").update(stable).digest("hex");
}

function writeEvolutionState(hash) {
  const output = {
    evolutionHash: hash,
    timestamp: new Date().toISOString()
  };

  fs.writeFileSync(
    path.join(__dirname, "evolution-state.json"),
    JSON.stringify(output, null, 2)
  );

  console.log("Evolution state updated:", hash);
}

function runEvolution() {
  const report = loadReport();
  const hash = computeEvolutionHash(report);
  writeEvolutionState(hash);
}

runEvolution();
