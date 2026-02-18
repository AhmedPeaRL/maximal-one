const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const REPORT_PATH = path.join(
  __dirname,
  "..",
  "publication-gate",
  "report.json"
);

function safeLoadJSON(filePath) {
  if (!fs.existsSync(filePath)) {
    console.log("Report not found. Evolution skipped.");
    process.exit(0);
  }

  const raw = fs.readFileSync(filePath, "utf-8").trim();

  if (!raw.startsWith("{") && !raw.startsWith("[")) {
    console.error("Invalid report.json: not valid JSON structure.");
    process.exit(1);
  }

  try {
    return JSON.parse(raw);
  } catch (err) {
    console.error("JSON parsing failed:", err.message);
    process.exit(1);
  }
}

function canonicalStringify(obj) {
  if (Array.isArray(obj)) {
    return `[${obj.map(canonicalStringify).join(",")}]`;
  }
  if (obj && typeof obj === "object") {
    return `{${Object.keys(obj)
      .sort()
      .map(k => `"${k}":${canonicalStringify(obj[k])}`)
      .join(",")}}`;
  }
  return JSON.stringify(obj);
}

function computeEvolutionHash(report) {
  const stable = canonicalStringify(report);
  return crypto.createHash("sha256").update(stable).digest("hex");
}

function writeEvolutionState(hash) {
  const output = {
    evolutionHash: hash
  };

  fs.writeFileSync(
    path.join(__dirname, "evolution-state.json"),
    JSON.stringify(output, null, 2)
  );

  console.log("Evolution state updated:", hash);
}

function runEvolution() {
  const report = safeLoadJSON(REPORT_PATH);
  const hash = computeEvolutionHash(report);
  writeEvolutionState(hash);
}

runEvolution();
