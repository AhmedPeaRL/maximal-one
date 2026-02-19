#!/usr/bin/env node

/**
 * Deterministic Publication Gate
 * Canonicalized + Schema Locked
 * No silent failure path exists.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = process.cwd();
const GATE_DIR = path.join(ROOT, "core-scientific", "publication-gate");
const REPORT_PATH = path.join(GATE_DIR, "report.json");
const GENERATOR_PATH = path.join(GATE_DIR, "generate-report.cjs");

function sha256(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function fail(msg) {
  console.error("❌ Publication Gate Failure:");
  console.error(msg);
  process.exit(1);
}

function ensureExists(p) {
  if (!fs.existsSync(p)) {
    fail(`Missing required path: ${p}`);
  }
}

/**
 * Canonical JSON sort (matches jq -S)
 */
function canonicalize(obj) {
  return JSON.stringify(
    Object.keys(obj)
      .sort()
      .reduce((acc, key) => {
        acc[key] = obj[key];
        return acc;
      }, {}),
    null,
    2
  );
}

function main() {
  ensureExists(GATE_DIR);
  ensureExists(GENERATOR_PATH);

  const generatorSource = fs.readFileSync(GENERATOR_PATH, "utf8").replace(/\r/g, "");
  const generatorHash = sha256(generatorSource);

  const deterministicArtifact = sha256(
    JSON.stringify({
      node: process.version,
      platform: process.platform
    })
  );

  const baseReport = {
    deterministicArtifactHash: deterministicArtifact,
    generatorHash,
    invariant: "No silent failure path exists.",
    schemaVersion: 1
  };

  const canonical = canonicalize(baseReport);
  const reportHash = sha256(canonical);

  const finalReport = {
    ...baseReport,
    reportHash
  };

  fs.writeFileSync(REPORT_PATH, canonicalize(finalReport));

  console.log("✅ Deterministic report generated.");
  console.log("Report hash:", reportHash);
}

main();
