#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const ATTRACTOR_DIR = path.join(ROOT, "core-scientific", "attractor-field");

const RAW_PATH = path.join(ATTRACTOR_DIR, "raw-history.json");
const STATE_PATH = path.join(ATTRACTOR_DIR, "statistical-state.json");
const REPORT_PATH = path.join(ROOT, "report.json");

/* ============================
   Utility
============================ */

function loadJSON(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function saveJSON(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, 2));
}

/* ============================
   Deterministic Score Extractor
============================ */

function extractScore(report) {
  if (!report || typeof report.score !== "number") {
    throw new Error("report.json must contain numeric 'score'");
  }
  return report.score;
}

/* ============================
   Welford Online Update
============================ */

function updateWelford(state, newValue) {
  const count = state.count + 1;
  const delta = newValue - state.mean;
  const mean = state.mean + delta / count;
  const delta2 = newValue - mean;
  const m2 = state.m2 + delta * delta2;

  const variance = count > 1 ? m2 / (count - 1) : 0;
  const stdDev = Math.sqrt(variance);

  return {
    ...state,
    count,
    mean,
    m2,
    stdDev
  };
}

/* ============================
   Z-Score
============================ */

function computeZ(score, mean, stdDev) {
  if (stdDev === 0) return 0;
  return (score - mean) / stdDev;
}

/* ============================
   Main Execution
============================ */

function main() {
  const raw = loadJSON(RAW_PATH);
  const state = loadJSON(STATE_PATH);
  const report = loadJSON(REPORT_PATH);

  const score = extractScore(report);

  // Append raw immutable history
  raw.scores.push({
    timestamp: new Date().toISOString(),
    score
  });

  // Update statistical state using Welford
  const newState = updateWelford(state, score);

  const zScore = computeZ(score, newState.mean, newState.stdDev);

  let decision = "accepted";

  if (newState.count < newState.minHistory) {
    decision = "provisional";
  } else if (zScore < newState.zThreshold) {
    decision = "rejected";
  }

  const finalState = {
    ...newState,
    lastDecision: decision
  };

  // Persist
  saveJSON(RAW_PATH, raw);
  saveJSON(STATE_PATH, finalState);

  // Console observability
  console.log("===== Adaptive Threshold (Proof-Grade) =====");
  console.log("Score:", score);
  console.log("Count:", finalState.count);
  console.log("Mean:", finalState.mean);
  console.log("StdDev:", finalState.stdDev);
  console.log("Z-Score:", zScore);
  console.log("Decision:", decision);
  console.log("============================================");

  // Hard gate
  if (decision === "rejected") {
    console.error("Statistical gate rejected this run.");
    process.exit(1);
  }
}

main();
