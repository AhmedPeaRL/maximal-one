const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function computeSelfMetric() {
  const reportPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "aggregated-report.json"
  );

  if (!fs.existsSync(reportPath)) {
    throw new Error(
      "aggregated-report.json not found. Publication gate is incomplete."
    );
  }

  const raw = fs.readFileSync(reportPath, "utf-8");
  const data = JSON.parse(raw);

  if (!Array.isArray(data)) {
    throw new Error("Aggregated report must be an array.");
  }

  // Deterministic structural score
  const structuralSignature = crypto
    .createHash("sha256")
    .update(JSON.stringify(data))
    .digest("hex");

  const metric = {
    timestamp: new Date().toISOString(),
    entries: data.length,
    structuralSignature,
  };

  const outputPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "self-metric.json"
  );

  fs.writeFileSync(outputPath, JSON.stringify(metric, null, 2));

  console.log("Self-metric generated.");
  console.log("Entries:", data.length);
  console.log("Structural signature:", structuralSignature);

  return metric;
}

module.exports = { computeSelfMetric };
