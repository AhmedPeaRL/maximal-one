const fs = require('fs');

const REPORT_PATH = './artifacts/canonical_report.json';

if (!fs.existsSync(REPORT_PATH)) {
  console.log(JSON.stringify({
    passed: false,
    reason: "missing_canonical_report"
  }));
  process.exit(0);
}

let report;
try {
  report = JSON.parse(fs.readFileSync(REPORT_PATH, 'utf8'));
} catch (err) {
  console.log(JSON.stringify({
    passed: false,
    reason: "invalid_json"
  }));
  process.exit(0);
}

if (!report.spectral_profile) {
  console.log(JSON.stringify({
    passed: false,
    reason: "missing_spectral_profile"
  }));
  process.exit(0);
}

const alpha = report.spectral_profile.estimated_alpha;
const std   = report.spectral_profile.bootstrap_std;

if (
  typeof alpha !== 'number' ||
  typeof std !== 'number' ||
  !isFinite(alpha) ||
  !isFinite(std) ||
  std <= 0
) {
  console.log(JSON.stringify({
    passed: false,
    reason: "invalid_numeric_input"
  }));
  process.exit(0);
}

const z = Math.abs((alpha - 0.5) / std);
const passed = z < 1;

console.log(JSON.stringify({
  alpha,
  std,
  z,
  passed,
  decision_rule: "z < 1 sigma (canonical_report anchored)"
}));
