#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const {
  shannonEntropy,
  transitionMatrix,
  driftCoefficient
} = require("./stability-metrics");
const { linearRegressionSlope } = require("./regression");
const { stabilityIndex } = require("./stability-index");

const ROOT = process.cwd();
const MEMORY_PATH = path.join(ROOT, ".coherence-memory", "state-history.jsonl");

function fail(msg) {
  console.error("❌ Dynamics Engine Failure:");
  console.error(msg);
  process.exit(1);
}

if (!fs.existsSync(MEMORY_PATH)) {
  fail("State history not found.");
}

const lines = fs.readFileSync(MEMORY_PATH, "utf8")
  .split("\n")
  .filter(Boolean);

const states = lines.map(line => JSON.parse(line));
const hashes = states.map(s => s.reportHash);

const entropy = shannonEntropy(hashes);
const transitions = transitionMatrix(hashes);
const drift = driftCoefficient(hashes);

const summary = {
  totalRuns: hashes.length,
  entropy,
  drift,
  transitionMatrix: transitions
};

console.log(JSON.stringify(summary, null, 2));

function extendedMetrics(scores, stdDev) {
  const slope = linearRegressionSlope(scores);
  const drift = driftCoefficient(scores);

  const stability = stabilityIndex({
    slope,
    drift,
    stdDev
  });

  return {
    slope,
    drift,
    stability
  };
}

module.exports = {
  extendedMetrics
};
