const fs = require("fs");

function readJson(path) {
  return JSON.parse(
    fs.readFileSync(path, "utf8")
  );
}

function finite(value) {
  return (
    typeof value === "number"
    &&
    Number.isFinite(value)
  );
}

function fail(message) {
  console.error(
    `❌ STRICT CONTRACT FAILURE: ${message}`
  );
  process.exit(1);
}

const report = readJson(
  "artifacts/canonical_report.json"
);

const claim = readJson(
  "core-scientific/strict_claim.json"
);

const expected =
  claim.expected_result;

const alpha =
  Number(
    report.spectral_profile.estimated_alpha
  );

const sigma =
  Number(
    report.spectral_profile.bootstrap_std
  );

const pValue =
  Number(
    report.statistical_test.p_value
  );

const methodDelta =
  Number(
    report.cross_method_validation.agreement_delta
  );

const scale =
  report.multi_scale_validation;

const scaleDispersion =
  Number(
    scale.dispersion ??
    scale.relative_spread
  );

const bootstrapDiscrepancy =
  Number(
    report.bootstrap_center_discrepancy.std_units
  );

const crossDomain =
  report.cross_domain_replication || {};

const crossDomainStd =
  Number(
    crossDomain.real_domain_std
  );

const independentDomains =
  Number(
    report.consensus_guard
      .independent_real_domains
  );

const [minAlpha, maxAlpha] =
  expected.alpha_range;

if (
  !finite(alpha)
  ||
  alpha < minAlpha
  ||
  alpha > maxAlpha
) {
  fail(
    `alpha=${alpha} outside [${minAlpha}, ${maxAlpha}]`
  );
}

if (
  !finite(sigma)
  ||
  sigma > Number(expected.max_sigma)
) {
  fail(
    `sigma=${sigma} exceeds ${expected.max_sigma}`
  );
}

if (
  !finite(pValue)
  ||
  pValue > Number(expected.max_p_value)
) {
  fail(
    `p_value=${pValue} exceeds ${expected.max_p_value}`
  );
}

if (
  !finite(methodDelta)
  ||
  methodDelta >
    Number(expected.max_method_delta)
) {
  fail(
    `method_delta=${methodDelta} exceeds ${expected.max_method_delta}`
  );
}

if (
  !finite(scaleDispersion)
  ||
  scaleDispersion >
    Number(expected.max_scale_dispersion)
) {
  fail(
    `scale_dispersion=${scaleDispersion} exceeds ${expected.max_scale_dispersion}`
  );
}

if (
  !finite(bootstrapDiscrepancy)
  ||
  bootstrapDiscrepancy >
    Number(
      expected.max_bootstrap_center_discrepancy_sigma
    )
) {
  fail(
    "bootstrap center discrepancy exceeds declared limit"
  );
}

if (
  !finite(crossDomainStd)
  ||
  crossDomainStd >
    Number(expected.max_cross_domain_std)
) {
  fail(
    `cross_domain_std=${crossDomainStd} exceeds ${expected.max_cross_domain_std}`
  );
}

if (
  independentDomains
  <
  Number(
    expected.min_independent_real_domains
  )
) {
  fail(
    `independent real domains=${independentDomains} below required minimum`
  );
}

if (
  scale.valid !== true
  ||
  scale.scale_invariant !== true
) {
  fail(
    "scale validation/invariance requirement failed"
  );
}

if (
  report.null_rejected !== true
) {
  fail(
    "primary null was not rejected"
  );
}

console.log(
  "✅ STRICT SCIENTIFIC CONTRACT PREREQUISITES PASSED"
);

console.log(
  "ℹ️ This does NOT independently promote the scientific claim."
);

console.log(
  "ℹ️ External reproducibility and adversarial evidence remain claim-level requirements."
);
