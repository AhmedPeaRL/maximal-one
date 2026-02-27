#!/usr/bin/env node

/**
 * Deterministic Publication Gate
 * Canonical + Stability Integrated
 * No silent failure path exists.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = process.cwd();
const GATE_DIR = path.join(ROOT, "core-scientific", "publication-gate");
const REPORT_PATH = path.join(GATE_DIR, "report.json");
const GENERATOR_PATH = path.join(GATE_DIR, "generate-report.cjs");

const MEMORY_DIR = path.join(ROOT, ".coherence-memory");
const STATE_HISTORY_PATH = path.join(MEMORY_DIR, "state-history.jsonl");

const { canonicalJSONStringify } = require("./utils/canonicalize");
const crypto = require("crypto");

const canonical = canonicalJSONStringify(report);

const hash = crypto
  .createHash("sha256")
  .update(canonical, "utf8")
  .digest("hex");

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

function ensureDir(p) {
  if (!fs.existsSync(p)) {
    fs.mkdirSync(p, { recursive: true });
  }
}

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

function appendState(state) {
  ensureDir(MEMORY_DIR);
  const line = JSON.stringify(state);
  fs.appendFileSync(STATE_HISTORY_PATH, line + "\n");
}

function main() {
  ensureExists(GATE_DIR);
  ensureExists(GENERATOR_PATH);

  const start = Date.now();

  const generatorSource = fs.readFileSync(GENERATOR_PATH, "utf8").replace(/\r/g, "");
  const generatorHash = sha256(generatorSource);

  const deterministicArtifactHash = sha256(
    JSON.stringify({
      node: process.version,
      platform: process.platform
    })
  );

  const baseReport = {
    deterministicArtifactHash,
    generatorHash,
    invariant: "No silent failure path exists.",
    schemaVersion: 2
  };

  const canonicalBase = canonicalize(baseReport);
  const baseString = JSON.stringify(canonicalBase);
  const reportHash = sha256(baseString);

  const finalReport = {
    ...baseReport,
    reportHash
  };

  const canonicalFinal = canonicalize(finalReport);
  const finalString = JSON.stringify(canonicalFinal, null, 2);

  require("fs").writeFileSync(
  "node_report.hash",
  hash + "\n",
  { encoding: "utf8" }
  );

  const durationMs = Date.now() - start;

  appendState({
    timestamp: new Date().toISOString(),
    reportHash,
    generatorHash,
    durationMs,
    nodeVersion: process.version,
    platform: process.platform
  });

  console.log("✅ Deterministic report generated.");
  console.log("Report hash:", reportHash);
}

main();
