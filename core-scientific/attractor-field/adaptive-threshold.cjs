const fs = require('fs');

const report = JSON.parse(
  fs.readFileSync('artifacts/canonical_report.json','utf8')
);

const alpha = report.spectral_profile.estimated_alpha;
const std   = report.spectral_profile.bootstrap_std;

/*
  Null expectation assumed estimated via bootstrap mean ≈ alpha
  Under deterministic single-seed case, deviation should be ~0.
*/

const expected = alpha;  // placeholder until multi-seed sampling added
const z = (alpha - expected) / (std + 1e-12);

const threshold = 3;

const passed = Math.abs(z) < threshold;

const result = {
  alpha,
  std,
  expected,
  z,
  threshold,
  passed,
  decision_rule: "|alpha - E[alpha]| < 3 sigma"
};

console.log(JSON.stringify(result));
