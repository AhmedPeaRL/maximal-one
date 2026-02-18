#!/usr/bin/env node

/**
 * Adaptive Threshold Gate
 * Deterministic + Generator Locked
 * No Silent Failure Path
 */

const fs = require("fs");
const path = require("path");

const SCORE = parseFloat(process.argv[2]);

if (isNaN(SCORE)) {
  console.error("Invalid score input.");
  process.exit(1);
}

const STATE_PATH = path.join(
  __dirname,
  "..",
  "state",
  "adaptive-baseline.json"
);

// Ensure state directory exists
fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });

let baseline = SCORE;
let slope = 0;
let threshold = SCORE;
let passed = true;

if (fs.existsSync(STATE_PATH)) {
  const prev = JSON.parse(fs.readFileSync(STATE_PATH, "utf8"));

  const alpha = 0.2; // smoothing factor
  baseline = alpha * SCORE + (1 - alpha) * prev.baseline;

  slope = baseline - prev.baseline;

  const minMargin = 0.01;
  const dynamicMargin = Math.max(minMargin, Math.abs(slope) * 0.5);

  threshold = baseline - dynamicMargin;

  passed = SCORE >= threshold;
}

// Persist deterministic state
fs.writeFileSync(
  STATE_PATH,
  JSON.stringify(
    {
      baseline,
      lastScore: SCORE,
      updatedAt: new Date().toISOString()
    },
    null,
    2
  )
);

const result = {
  score: SCORE,
  baseline,
  threshold,
  slope,
  passed
};

console.log(JSON.stringify(result));
