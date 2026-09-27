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

const methodDelta =
  Number(
    report.cross_method_validation.agreement_delta
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
    crossDomain.independent_secondary_real_domains
    ?? 0
  );

const [minAlpha, maxAlpha] =
  expected.alpha_range;

/*
 * ------------------------------------------------------------
 * 1. Canonical alpha range
 * ------------------------------------------------------------
 */

if (
  !finite(alpha) ||
  alpha < minAlpha ||
  alpha > maxAlpha
) {
  fail(
    `alpha=${alpha} outside [${minAlpha}, ${maxAlpha}]`
  );
}

/*
 * ------------------------------------------------------------
 * 2. Bootstrap uncertainty bound
 * ------------------------------------------------------------
 */

if (
  !finite(sigma) ||
  sigma > Number(expected.max_sigma)
) {
  fail(
    `sigma=${sigma} exceeds ${expected.max_sigma}`
  );
}

/*
 * ------------------------------------------------------------
 * 3. Cross-method agreement
 *
 * Welch vs independent FFT is a declared validation layer.
 * ------------------------------------------------------------
 */

if (
  !finite(methodDelta) ||
  methodDelta >
    Number(expected.max_method_delta)
) {
  fail(
    `method_delta=${methodDelta} exceeds ${expected.max_method_delta}`
  );
}

/*
 * ------------------------------------------------------------
 * 4. Bootstrap center consistency
 * ------------------------------------------------------------
 */

if (
  !finite(bootstrapDiscrepancy) ||
  bootstrapDiscrepancy >
    Number(
      expected.max_bootstrap_center_discrepancy_sigma
    )
) {
  fail(
    "bootstrap center discrepancy exceeds declared limit"
  );
}

/*
 * ------------------------------------------------------------
 * 5. Independent real-domain replication
 * ------------------------------------------------------------
 */

if (
  !finite(crossDomainStd) ||
  crossDomainStd >
    Number(expected.max_cross_domain_std)
) {
  fail(
    `cross_domain_std=${crossDomainStd} exceeds ${expected.max_cross_domain_std}`
  );
}

if (
  independentDomains <
  Number(
    expected.min_independent_secondary_real_domains
  )
) {
  fail(
    `independent secondary real domains=${independentDomains} below required minimum`
  );
}

/*
 * ------------------------------------------------------------
 * 6. PRIMARY SCIENTIFIC NULL GATE
 *
 * This is the authoritative null for claim support.
 *
 * IMPORTANT:
 *
 * report.statistical_test.p_value is the permutation-null
 * diagnostic and is NOT the primary scientific null.
 *
 * The authoritative result is:
 *
 * report.appropriate_stochastic_null
 *
 * Therefore this gate must NEVER read:
 *
 *     report.null_rejected
 *
 * and must NEVER promote the permutation-null result.
 * ------------------------------------------------------------
 */

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

if (
  stochasticNull.reject_at_0_05 !== true
) {
  const pValue =
    Number(
      stochasticNull.p_value_mc_add_one
    );

  fail(
    `primary appropriate stochastic null was not rejected (p=${pValue})`
  );
}


/*
 * ------------------------------------------------------------
 * 7. Explicit epistemic separation
 *
 * Scale stability and permutation-null rejection are
 * diagnostic layers, not claim-promotion gates.
 *
 * Their presence or absence must not alter this contract.
 * ------------------------------------------------------------
 */

console.log(
  "✅ STRICT SCIENTIFIC CONTRACT PASSED"
);

console.log(
  "ℹ️ Authoritative primary null: appropriate_stochastic_null"
);

console.log(
  "ℹ️ Permutation-null result is diagnostic-only."
);

console.log(
  "ℹ️ Scale stability is diagnostic-only."
);

console.log(
  "ℹ️ This contract does NOT independently promote the scientific claim."
);

console.log(
  "ℹ️ External reproducibility and adversarial evidence remain claim-level requirements."
);
