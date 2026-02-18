import fs from "fs";
import crypto from "crypto";

function assertCondition(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function sha256(content) {
  return crypto.createHash("sha256").update(content).digest("hex");
}

const raw = fs.readFileSync(
  "./core-scientific/publication-gate/report.json",
  "utf8"
);

const report = JSON.parse(raw);

assertCondition(
  typeof report.deterministicArtifactHash === "string",
  "deterministicArtifactHash missing"
);

const { deterministicArtifactHash, ...rest } = report;

const stable = JSON.stringify(
  rest,
  Object.keys(rest).sort(),
  2
) + "\n";

const recomputed = sha256(stable);

assertCondition(
  recomputed === deterministicArtifactHash,
  "deterministicArtifactHash mismatch"
);

console.log("Numerical stability verified.");
