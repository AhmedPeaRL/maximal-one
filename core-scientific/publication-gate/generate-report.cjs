#!/usr/bin/env node
/**
 * HCM Publication Gate – Deterministic Generator (Fully Locked)
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const root = path.resolve(__dirname, "../../");
const outputPath = path.join(__dirname, "report.json");
const generatorPath = __filename;

function sha256(content) {
  return crypto.createHash("sha256").update(content).digest("hex");
}

function readFileSafe(p) {
  return fs.readFileSync(p, "utf8").replace(/\r\n/g, "\n");
}

/* -------------------------
   1) Generator Lock
-------------------------- */
const generatorSource = readFileSafe(generatorPath);
const generatorHash = sha256(generatorSource);

/* -------------------------
   2) Deterministic Data
-------------------------- */
const packagePath = path.join(root, "package.json");
const packageJson = JSON.parse(readFileSafe(packagePath));

const baseReport = {
  system: "HCM",
  layer: "publication-gate",
  version: packageJson.version || "0.0.0",
  nodeVersion: process.version,
  platform: process.platform,
  generatorHash
};

/* -------------------------
   3) Deterministic Serialization
-------------------------- */
const stableBase = JSON.stringify(baseReport, Object.keys(baseReport).sort(), 2) + "\n";
const deterministicArtifactHash = sha256(stableBase);

/* -------------------------
   4) Final Object (Sorted)
-------------------------- */
const finalObject = {
  ...baseReport,
  deterministicArtifactHash
};

const finalOutput =
  JSON.stringify(finalObject, Object.keys(finalObject).sort(), 2) + "\n";

fs.writeFileSync(outputPath, finalOutput);

console.log("Deterministic artifact generated.");
console.log("Generator SHA256:", generatorHash);
console.log("Deterministic Artifact SHA256:", deterministicArtifactHash);
