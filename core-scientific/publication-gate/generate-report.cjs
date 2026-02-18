#!/usr/bin/env node
/**
 * HCM Publication Gate – Deterministic Generator (Generator Locked Version)
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
   1) Hash generator itself
-------------------------- */
const generatorSource = readFileSafe(generatorPath);
const generatorHash = sha256(generatorSource);

/* -------------------------
   2) Collect deterministic data
-------------------------- */

const packagePath = path.join(root, "package.json");
const packageJson = JSON.parse(readFileSafe(packagePath));

const report = {
  system: "HCM",
  layer: "publication-gate",
  version: packageJson.version || "0.0.0",
  timestampUTC: new Date().toISOString(),
  generatorHash: generatorHash,
  nodeVersion: process.version,
  platform: process.platform
};

/* -------------------------
   3) Deterministic serialization
-------------------------- */

const stableJson = JSON.stringify(report, Object.keys(report).sort(), 2) + "\n";
const reportHash = sha256(stableJson);

/* -------------------------
   4) Final write
-------------------------- */

const finalOutput = JSON.stringify(
  { ...report, reportHash },
  Object.keys({ ...report, reportHash }).sort(),
  2
) + "\n";

fs.writeFileSync(outputPath, finalOutput);

console.log("Report generated deterministically.");
console.log("Generator SHA256:", generatorHash);
console.log("Report SHA256:", reportHash);
