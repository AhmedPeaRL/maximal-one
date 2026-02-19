#!/usr/bin/env node

/**
 * Maximal-One Attractor Field Gate Engine
 * Version: 2.0 - Statistical Coherence Mode
 *
 * Purpose:
 * Transform attractor score validation into statistically grounded field evaluation.
 *
 * Logic:
 * - Accept dynamic input score
 * - Compare against adaptive statistical distribution
 * - Return structured evaluation result
 *
 * No randomness.
 * Fully deterministic.
 * Field-consistent.
 */

const fs = require('fs');
const path = require('path');

const score = parseFloat(process.argv[2]);

if (isNaN(score)) {
  console.error(JSON.stringify({
    passed: false,
    reason: "Invalid score input",
    threshold: null,
    statistical_context: null
  }));
  process.exit(1);
}

/**
 * Load historical attractor distribution
 */
const historyPath = path.join(__dirname, '../../state/attractor-history.json');

let history = [];

if (fs.existsSync(historyPath)) {
  history = JSON.parse(fs.readFileSync(historyPath, 'utf8'));
}

/**
 * If insufficient history → bootstrap threshold
 */
if (history.length < 10) {

  const bootstrapThreshold = 0.5;

  const result = {
    passed: score >= bootstrapThreshold,
    threshold: bootstrapThreshold,
    statistical_context: "bootstrap_mode",
    input_score: score
  };

  console.log(JSON.stringify(result));
  process.exit(0);
}

/**
 * Compute statistical properties
 */
const mean = history.reduce((a, b) => a + b, 0) / history.length;

const variance = history.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / history.length;

const stdDev = Math.sqrt(variance);

/**
 * Adaptive threshold rule:
 * threshold = mean + 0.25 * stdDev
 *
 * This ensures evolution is allowed only
 * when new score exceeds statistical attractor drift.
 */
const adaptiveThreshold = mean + (0.25 * stdDev);

/**
 * Evaluation
 */
const passed = score >= adaptiveThreshold;

/**
 * Append current score to history
 */
history.push(score);

fs.mkdirSync(path.dirname(historyPath), { recursive: true });
fs.writeFileSync(historyPath, JSON.stringify(history, null, 2));

/**
 * Output structured evaluation
 */
const result = {
  passed,
  threshold: adaptiveThreshold,
  input_score: score,
  mean,
  stdDev,
  statistical_context: "adaptive_field_mode"
};

console.log(JSON.stringify(result));
