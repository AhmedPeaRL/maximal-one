const fs = require('fs');
const path = require('path');

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
  const threshold = baseline !== null ? baseline - TOLERANCE : score - TOLERANCE;

  console.log(JSON.stringify({
    score,
    baseline,
    threshold,
    passed: score >= threshold
  }));
}

main();
