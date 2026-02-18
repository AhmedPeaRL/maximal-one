#!/usr/bin/env node

/**
 * Adaptive Threshold Gate
 * ESM Deterministic Mode
 * Baseline freezes on breakthrough only
 * No silent failure path
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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

fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });

let baseline = SCORE;
let threshold = SCORE;
let slope = 0;
let passed = true;

const BREAKTHROUGH_MARGIN = 0.02;
const STABILITY_MARGIN = 0.01;

if (fs.existsSync(STATE_PATH)) {
  const prev = JSON.parse(fs.readFileSync(STATE_PATH, "utf8"));

  baseline = prev.baseline;

  slope = SCORE - baseline;

  if (SCORE > baseline + BREAKTHROUGH_MARGIN) {
    baseline = SCORE; // freeze only on real breakthrough
  }

  threshold = baseline - STABILITY_MARGIN;

  passed = SCORE >= threshold;
}

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
