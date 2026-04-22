const fs = require("fs");

const report = JSON.parse(
  fs.readFileSync("artifacts/canonical_report.json", "utf8")
);

const claim = JSON.parse(
  fs.readFileSync("core-scientific/strict_claim.json", "utf8")
);

const alpha = report.spectral_profile.estimated_alpha;
const sigma = report.spectral_profile.bootstrap_std;

const [minA, maxA] = claim.expected_result.alpha_range;

if (alpha < minA || alpha > maxA || sigma > claim.expected_result.max_sigma) {
  console.error("❌ STRICT CLAIM FAILED");
  process.exit(1);
}

console.log("✅ STRICT CLAIM PASSED");
