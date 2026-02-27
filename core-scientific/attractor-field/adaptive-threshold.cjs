const fs = require('fs');

const report = JSON.parse(
  fs.readFileSync('artifacts/canonical_report.json','utf8')
);

const alpha = report.spectral_profile.estimated_alpha;
const std   = report.spectral_profile.bootstrap_std;

/*
  Define z-score properly as standardized deviation
  relative to expected baseline.
  We assume baseline mean ≈ 0 under null stability.
*/

const z = alpha / (std + 1e-12);

/*
  Scientifically reasonable bound:
  |z| < 3  → within 3-sigma envelope
*/

const threshold = 3;

const passed = Math.abs(z) < threshold;

const result = {
  alpha,
  std,
  z,
  threshold,
  passed,
  decision_rule: "|z| < 3 sigma envelope"
};

console.log(JSON.stringify(result));
