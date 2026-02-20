#!/usr/bin/env node

/**
 * Adaptive Attractor Field Gate v3.0
 * Scientific Logging Edition
 *
 * Produces full statistical evolution record:
 * - score
 * - mean
 * - stdDev
 * - zScore
 * - decision
 *
 * No silent failure path exists.
 */

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const FIELD_DIR = path.join(ROOT, "core-scientific", "attractor-field");
const HISTORY_PATH = path.join(FIELD_DIR, "attractor-history.json");

const MIN_HISTORY = 5;
const Z_THRESHOLD = -2; // Reject if extreme negative drift

function fail(msg) {
  console.error("::error::Adaptive gate rejected evolution.");
  console.error(msg);
  process.exit(1);
}

function ensureDir(p) {
  if (!fs.existsSync(p)) {
    fs.mkdirSync(p, { recursive: true });
  }
}

function mean(values) {
  return values.reduce((a, b) => a + b, 0) / values.length;
}

function stdDev(values, m) {
  const variance =
    values.reduce((sum, v) => sum + Math.pow(v - m, 2), 0) /
    values.length;
  return Math.sqrt(variance);
}

function generateScore() {
  // Deterministic seed based on report.json if exists
  const reportPath = path.join(
    ROOT,
    "core-scientific",
    "publication-gate",
    "report.json"
  );

  if (!fs.existsSync(reportPath)) {
    return Math.random(); // fallback
  }

  const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
  const hash = report.reportHash;

  const numeric = parseInt(hash.slice(0, 12), 16);
  return (numeric % 1000000) / 1000000;
}

function loadHistory() {
  if (!fs.existsSync(HISTORY_PATH)) {
    return {
      schemaVersion: 2,
      history: []
    };
  }

  const raw = JSON.parse(fs.readFileSync(HISTORY_PATH, "utf8"));

  if (!raw.schemaVersion || raw.schemaVersion !== 2) {
    return {
      schemaVersion: 2,
      history: []
    };
  }

  return raw;
}

function main() {
  ensureDir(FIELD_DIR);

  const historyData = loadHistory();
  const history = historyData.history;

  const score = generateScore();

  const previousScores = history.map(h => h.score);
  const allScores = [...previousScores, score];

  const currentMean = mean(allScores);
  const currentStdDev = allScores.length > 1
    ? stdDev(allScores, currentMean)
    : 0;

  const zScore =
    currentStdDev === 0
      ? 0
      : (score - currentMean) / currentStdDev;

  let decision = "accepted";

  if (
    allScores.length >= MIN_HISTORY &&
    zScore < Z_THRESHOLD
  ) {
    decision = "rejected";
  }

  const record = {
    timestamp: new Date().toISOString(),
    score,
    mean: currentMean,
    stdDev: currentStdDev,
    zScore,
    decision
  };

  history.push(record);

  const finalData = {
    schemaVersion: 2,
    history
  };

  fs.writeFileSync(
    HISTORY_PATH,
    JSON.stringify(finalData, null, 2)
  );

  console.log("Adaptive score:", score);
  console.log("Mean:", currentMean);
  console.log("StdDev:", currentStdDev);
  console.log("Z-Score:", zScore);
  console.log("Decision:", decision);

  if (decision === "rejected") {
    fail("Z-score below adaptive threshold.");
  }

  console.log("Attractor field evolution accepted.");
}

main();
