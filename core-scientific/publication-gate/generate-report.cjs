#!/usr/bin/env node

import fs from "fs";
import crypto from "crypto";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function sha256(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

function canonicalStringify(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort(), 2);
}

const generatorSource = fs.readFileSync(__filename, "utf8").replace(/\r/g, "");
const generatorHash = sha256(generatorSource);

// ===== Deterministic Artifact Definition =====
const deterministicArtifact = {
  model: "maximal-one",
  version: "1.0.0",
  invariant: "No silent failure path exists.",
  generatorLocked: true
};

const deterministicArtifactString = canonicalStringify(deterministicArtifact);
const deterministicArtifactHash = sha256(deterministicArtifactString);

// ===== Report Object WITHOUT reportHash =====
const report = {
  deterministicArtifact,
  deterministicArtifactHash,
  generatorHash
};

// Canonical serialize BEFORE hashing
const canonicalReportString = canonicalStringify(report);
const reportHash = sha256(canonicalReportString);

// Attach final hash
report.reportHash = reportHash;

// Final canonical write
const finalString = canonicalStringify(report);

fs.writeFileSync(
  path.join(__dirname, "report.json"),
  finalString + "\n",
  "utf8"
);

console.log("Deterministic artifact generated.");
console.log("Generator SHA256:", generatorHash);
console.log("Deterministic Artifact SHA256:", deterministicArtifactHash);
console.log("Report SHA256:", reportHash);
