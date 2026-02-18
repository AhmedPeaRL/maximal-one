import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HISTORY_FILE = path.join(__dirname, 'attractor-history.json');

const ALPHA = 0.4;          // exponential smoothing factor
const TOLERANCE = 0.02;     // adaptive tolerance band
const MAX_DELTA = 0.15;     // entropy spike guard

function readHistory() {
  if (!fs.existsSync(HISTORY_FILE)) return [];
  return JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf8'));
}

function writeHistory(history) {
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
}

function exponentialMovingAverage(arr) {
  if (arr.length === 0) return null;

  let ema = arr[0];
  for (let i = 1; i < arr.length; i++) {
    ema = ALPHA * arr[i] + (1 - ALPHA) * ema;
  }

  return ema;
}

function emaSlope(arr) {
  if (arr.length < 2) return 0;

  let emaPrev = arr[0];
  let emaCurrent = arr[0];

  for (let i = 1; i < arr.length; i++) {
    emaCurrent = ALPHA * arr[i] + (1 - ALPHA) * emaPrev;
    emaPrev = emaCurrent;
  }

  const lastRaw = arr[arr.length - 1];
  const previousRaw = arr[arr.length - 2];

  return lastRaw - previousRaw;
}

function main() {
  const score = parseFloat(process.argv[2]);

  if (isNaN(score)) {
    console.error("Invalid score input");
    process.exit(1);
  }

  const history = readHistory();

  const last = history.length > 0
    ? history[history.length - 1]
    : score;

  if (Math.abs(score - last) > MAX_DELTA) {
    console.log(JSON.stringify({
      score,
      baseline: null,
      threshold: null,
      slope: null,
      passed: false,
      reason: "entropy spike detected"
    }));
    process.exit(1);
  }

  history.push(score);
  writeHistory(history);

  const baseline = exponentialMovingAverage(history);
  const slope = emaSlope(history);

  const threshold = baseline !== null
    ? baseline - TOLERANCE
    : score - TOLERANCE;

  const passed = score >= threshold;

  console.log(JSON.stringify({
    score,
    baseline,
    threshold,
    slope,
    passed
  }));
}

main();
