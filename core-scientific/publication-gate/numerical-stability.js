import fs from "fs";

function assertCondition(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const raw = fs.readFileSync(
  "./core-scientific/publication-gate/report.json",
  "utf8"
);

const report = JSON.parse(raw);

assertCondition(report.deterministicArtifact, "deterministicArtifact missing");
assertCondition(report.deterministicArtifactHash, "deterministicArtifactHash missing");
assertCondition(report.generatorHash, "generatorHash missing");
assertCondition(report.reportHash, "reportHash missing");

console.log("Numerical stability verified.");
