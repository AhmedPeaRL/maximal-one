#!/usr/bin/env node

/**
 * Proof-Grade Adaptive Threshold
 * Deterministic
 * Welford Online Variance
 * Burn-in Discipline
 * Recompute Mode Integrity
 */

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const FIELD_DIR = path.join(ROOT, "core-scientific", "attractor-field");

const RAW_PATH = path.join(FIELD_DIR, "raw-history.json");
const STATE_PATH = path.join(FIELD_DIR, "statistical-state.json");

const BURN_IN = 5;
const EPSILON = 1e-12;

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function ensure(p, fallback) {
  if (!fs.existsSync(p)) {
    fs.writeFileSync(p, JSON.stringify(fallback, null, 2));
  }
}

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function writeJSON(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, 2));
}

/**
 * Welford recomputation from raw history
 */
function recomputeFromRaw(scores) {
  let mean = 0;
  let m2 = 0;
  let count = 0;

  for (const x of scores) {
    count++;
    const delta = x - mean;
    mean += delta / count;
    const delta2 = x - mean;
    m2 += delta * delta2;
  }

  const variance = count > 1 ? m2 / (count - 1) : 0;
  const stdDev = Math.sqrt(variance);

  return { count, mean, m2, stdDev };
}

function main() {
  ensure(FIELD_DIR, {});
  ensure(RAW_PATH, { scores: [] });
  ensure(STATE_PATH, { count: 0, mean: 0, m2: 0 });

  const raw = readJSON(RAW_PATH);
  const state = readJSON(STATE_PATH);

  const scores = raw.scores || [];

  // deterministic score derived from report hash
  const report = readJSON(
    path.join(ROOT, "core-scientific", "publication-gate", "report.json")
  );

  const score =
    parseInt(report.reportHash.slice(0, 12), 16) / 0xffffffffffff;

  scores.push(score);

  // recompute full state
  const recomputed = recomputeFromRaw(scores);

  // corruption detection
  if (
    Math.abs(recomputed.mean - state.mean) > EPSILON &&
    state.count > 0
  ) {
    fail("Statistical state drift detected.");
  }

  // update files
  raw.scores = scores;
  writeJSON(RAW_PATH, raw);

  writeJSON(STATE_PATH, {
    count: recomputed.count,
    mean: recomputed.mean,
    m2: recomputed.m2,
  });

  const zScore =
    recomputed.stdDev > 0
      ? (score - recomputed.mean) / recomputed.stdDev
      : 0;

  const burnInComplete = recomputed.count >= BURN_IN;

  const passed =
    burnInComplete
      ? Math.abs(zScore) <= 3
      : true;

  const result = {
    score,
    mean: recomputed.mean,
    stdDev: recomputed.stdDev,
    zScore,
    count: recomputed.count,
    burnInComplete,
    passed,
  };

  // human readable log
  console.log("Adaptive score:", score.toFixed(6));
  console.log("Mean:", recomputed.mean.toFixed(6));
  console.log("StdDev:", recomputed.stdDev.toFixed(6));
  console.log("Z-Score:", zScore.toFixed(6));
  console.log("Count:", recomputed.count);
  console.log("Burn-in complete:", burnInComplete);
  console.log("Decision:", passed ? "accepted" : "rejected");

  // machine contract (IMPORTANT)
  process.stdout.write("\n" + JSON.stringify(result));
}

main();
