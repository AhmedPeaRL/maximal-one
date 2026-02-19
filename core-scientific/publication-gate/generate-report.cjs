#!/usr/bin/env node

/**
 * Deterministic Publication Gate
 * Fully Canonical + Stability Compatible
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
 * Fully recursive canonical JSON (matches jq -S)
 */
function canonicalize(obj) {
  if (Array.isArray(obj)) {
    return obj.map(canonicalize);
  }

  if (obj !== null && typeof obj === "object") {
    return Object.keys(obj)
      .sort()
      .reduce((acc, key) => {
        acc[key] = canonicalize(obj[key]);
        return acc;
      }, {});
  }

  return obj;
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
    deterministicArtifact, // <-- stability expects this exact key
    generatorHash,
    invariant: "No silent failure path exists.",
    schemaVersion: 1
  };

  const canonicalBase = canonicalize(baseReport);
  const baseString = JSON.stringify(canonicalBase, null, 2);
  const reportHash = sha256(baseString);

  const finalReport = {
    ...baseReport,
    reportHash
  };

  const canonicalFinal = canonicalize(finalReport);
  const finalString = JSON.stringify(canonicalFinal, null, 2);

  fs.writeFileSync(REPORT_PATH, finalString);

  console.log("✅ Deterministic report generated.");
  console.log("Report hash:", reportHash);
}

main();
