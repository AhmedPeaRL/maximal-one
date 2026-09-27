const fs = require("fs");

function readJson(path) {
  return JSON.parse(
    fs.readFileSync(path, "utf8")
  );
}

function finite(value) {
  return (
    typeof value === "number" &&
    Number.isFinite(value)
  );
}

function fail(message) {
  console.error(
    `❌ CLAIM PROMOTION BLOCKED: ${message}`
  );

  process.exit(1);
}

const report = readJson(
  "artifacts/canonical_report.json"
);

const claim = readJson(
  "core-scientific/strict_claim.json"
);

const stochasticNull =
  report.appropriate_stochastic_null;

if (
  !stochasticNull ||
  typeof stochasticNull !== "object"
) {
  fail(
    "appropriate_stochastic_null result is missing"
  );
}

if (
  stochasticNull.valid !== true
) {
  fail(
    "appropriate stochastic null result is invalid"
  );
}

if (
  stochasticNull.support_eligible !== true
) {
  fail(
    "appropriate stochastic null is not support-eligible"
  );
}

const pValue =
  Number(
    stochasticNull.p_value_mc_add_one
  );

if (!finite(pValue)) {
  fail(
    "primary stochastic-null p-value is not finite"
  );
}

if (
  stochasticNull.reject_at_0_05 !== true
) {
  fail(
    `primary appropriate stochastic null was not rejected (p=${pValue})`
  );
}

const interpretation =
  report.scientific_interpretation || {};

if (
  interpretation.claim_support_gate !== true
) {
  fail(
    "canonical scientific claim-support gate is closed"
  );
}

const reproducibility =
  interpretation.reproducibility || {};

if (
  reproducibility.independent_rerun !==
  "verified"
) {
  fail(
    "independent rerun is not verified"
  );
}

if (
  reproducibility.fingerprint_match !== true
) {
  fail(
    "fingerprint match is not verified"
  );
}

console.log(
  "✅ CLAIM PROMOTION PREREQUISITES SATISFIED"
);

console.log(
  `Primary stochastic-null p-value: ${pValue}`
);

console.log(
  "Scientific claim may proceed to independent review."
);

console.log(
  `Claim title: ${claim.title}`
);
