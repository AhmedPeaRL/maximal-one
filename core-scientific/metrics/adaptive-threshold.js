import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HISTORY_FILE = path.join(__dirname, 'attractor-history.json');
const WINDOW = 5;
const TOLERANCE = 0.02;

function readHistory() {
  if (!fs.existsSync(HISTORY_FILE)) return [];
  return JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf8'));
}

function writeHistory(history) {
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
}

function movingAverage(arr) {
  if (arr.length === 0) return null;
  const recent = arr.slice(-WINDOW);
  const sum = recent.reduce((a, b) => a + b, 0);
  return sum / recent.length;
}

function slope(arr) {
  if (arr.length < 2) return 0;
  const recent = arr.slice(-WINDOW);
  let delta = 0;
  for (let i = 1; i < recent.length; i++) {
    delta += recent[i] - recent[i - 1];
  }
  return delta / (recent.length - 1);
}

function main() {
  const score = parseFloat(process.argv[2]);

  if (isNaN(score)) {
    console.error("Invalid score input");
    process.exit(1);
  }

  const history = readHistory();
  history.push(score);
  writeHistory(history);

  const baseline = movingAverage(history);
  const trend = slope(history);

  const threshold = baseline !== null
    ? baseline - TOLERANCE
    : score - TOLERANCE;

  const passed = score >= threshold;

  const MAX_DELTA = 0.15;
  const last = history.length > 1 ? history[history.length - 2] : score;
  
  if (Math.abs(score - last) > MAX_DELTA) {
    console.log(JSON.stringify({
      score,
      baseline,
      threshold,
      slope: trend,
      passed: false,
      reason: "entropy spike detected"
    }));
    process.exit(1);
  }

main();
