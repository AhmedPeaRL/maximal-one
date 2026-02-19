#!/usr/bin/env node
/**
 * HCM Publication Gate – Deterministic Generator (Generator Locked Version)
 */
const fs = require('fs');
const crypto = require('crypto');

const generatorPath = __filename;
const reportPath = __dirname + '/report.json';

// Helper: stable stringify (sorted keys)
function stableStringify(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort(), 2);
}

// 1) Read generator file and compute its SHA256 (normalized line endings)
const generatorSource = fs.readFileSync(generatorPath, 'utf8').replace(/\r/g, '');
const generatorHash = crypto.createHash('sha256').update(generatorSource).digest('hex');

// 2) Build deterministic payload (WITHOUT reportHash)
const payload = {
  version: "1.0.0",
  generatorHash,
  timestamp: "LOCKED-DETERMINISTIC",
  system: "HCM-Truth-Lock"
};

// 3) Compute report hash using stable sorted JSON
const canonical = stableStringify(payload);
const reportHash = crypto.createHash('sha256').update(canonical).digest('hex');

// 4) Final object
const finalReport = {
  ...payload,
  reportHash
};

// 5) Write deterministically
fs.writeFileSync(reportPath, stableStringify(finalReport) + '\n');

console.log("Deterministic artifact generated.");
console.log("Generator SHA256:", generatorHash);
console.log("Deterministic Artifact SHA256:", reportHash);
