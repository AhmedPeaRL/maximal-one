#!/usr/bin/env node

/**
 * Adaptive Threshold Engine
 * Deterministic.
 * History-aware.
 * No silent fallback path exists.
 */

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const HISTORY_PATH = path.join(
  ROOT,
  "core-scientific",
  "metrics",
  "attractor-history.json"
);

function fail(msg) {
  console.error("❌ Adaptive Threshold Failure:");
  console.error(msg);
  process.exit(1);
}

function median(values) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 !== 0
    ? sorted[mid]
    : (sorted[mid - 1] + sorted[mid]) / 2;
}

function main() {
  const inputScore = parseFloat(process.argv[2]);

  if (isNaN(inputScore)) {
    fail("Invalid score input.");
  }

  if (!fs.existsSync(HISTORY_PATH)) {
    fail("Missing attractor-history.json");
  }

  const history = JSON.parse(
    fs.readFileSync(HISTORY_PATH, "utf8")
  );

  if (!Array.isArray(history)) {
    fail("History must be an array.");
  }

  const recentWindow = history.slice(-10);
  const baseline = median(recentWindow);

  if (baseline === null) {
    fail("Cannot compute baseline from empty history.");
  }

  const previous =
    history.length >= 2
      ? history[history.length - 2]
      : baseline;

  const slope = inputScore - previous;

  const threshold = baseline + slope * 0.25;

  const passed = inputScore >= threshold;

  const result = {
    score: inputScore,
    baseline,
    threshold,
    slope,
    passed
  };

  console.log(JSON.stringify(result));
}

main();
