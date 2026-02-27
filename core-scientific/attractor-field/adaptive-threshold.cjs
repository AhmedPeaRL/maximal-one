const fs = require('fs');

const data = JSON.parse(
  fs.readFileSync('./core-scientific/repro-core/spectral-profile.json', 'utf8')
);

const alpha = data.estimated_alpha;
const std = data.bootstrap_std;

if (typeof alpha !== 'number' || typeof std !== 'number') {
  console.log(JSON.stringify({ passed: false, reason: "invalid_input" }));
  process.exit(0);
}

// z-score relative to reference 0.5
const z = Math.abs((alpha - 0.5) / std);

// decision rule: within 1 sigma
const passed = z < 1;

console.log(JSON.stringify({
  alpha,
  std,
  z,
  passed,
  decision_rule: "z < 1 sigma"
}));
