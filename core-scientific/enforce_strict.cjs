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

function assert(condition, message) {
  if (!condition) {
    fail(message);
  }
}

function exists(path) {
  return fs.existsSync(path);
}

const REPORT_PATH =
  "artifacts/canonical_report.json";

const CLAIM_PATH =
  "core-scientific/strict_claim.json";

const REPLAY_PATH =
  "artifacts/external_replay_verification.json";

const ADVERSARIAL_PATH =
  "artifacts/adversarial_control.json";

assert(
  exists(REPORT_PATH),
  `missing ${REPORT_PATH}`
);

assert(
  exists(CLAIM_PATH),
  `missing ${CLAIM_PATH}`
);

const report = readJson(
  REPORT_PATH
);

const claim = readJson(
  CLAIM_PATH
);

const expected =
  claim.expected_result;

assert(
  expected &&
  typeof expected === "object",
  "strict_claim.expected_result is missing"
);

/*
 * ------------------------------------------------------------
 * 1. CANONICAL ALPHA
 * ------------------------------------------------------------
 */

const alpha =
  Number(
    report?.spectral_profile?.estimated_alpha
  );

const [minAlpha, maxAlpha] =
  expected.alpha_range;

assert(
  finite(alpha),
  `canonical alpha is not finite: ${alpha}`
);

assert(
  alpha >= Number(minAlpha) &&
  alpha <= Number(maxAlpha),
  (
    `canonical alpha=${alpha} outside ` +
    `[${minAlpha}, ${maxAlpha}]`
  )
);

/*
 * ------------------------------------------------------------
 * 2. BOOTSTRAP UNCERTAINTY
 * ------------------------------------------------------------
 */

const sigma =
  Number(
    report?.spectral_profile?.bootstrap_std
  );

assert(
  finite(sigma),
  `bootstrap sigma is not finite: ${sigma}`
);

assert(
  sigma <= Number(expected.max_sigma),
  (
    `bootstrap sigma=${sigma} exceeds ` +
    `${expected.max_sigma}`
  )
);

/*
 * ------------------------------------------------------------
 * 3. CROSS-METHOD AGREEMENT
 * ------------------------------------------------------------
 */

const methodDelta =
  Number(
    report?.cross_method_validation
      ?.agreement_delta
  );

assert(
  finite(methodDelta),
  "cross-method delta is not finite"
);

assert(
  methodDelta <=
    Number(expected.max_method_delta),
  (
    `method delta=${methodDelta} exceeds ` +
    `${expected.max_method_delta}`
  )
);

/*
 * ------------------------------------------------------------
 * 4. BOOTSTRAP CENTER CONSISTENCY
 * ------------------------------------------------------------
 */

const bootstrapDiscrepancy =
  Number(
    report?.bootstrap_center_discrepancy
      ?.std_units
  );

assert(
  finite(bootstrapDiscrepancy),
  "bootstrap center discrepancy is not finite"
);

assert(
  bootstrapDiscrepancy <=
    Number(
      expected.max_bootstrap_center_discrepancy_sigma
    ),
  "bootstrap center discrepancy exceeds declared limit"
);

/*
 * ------------------------------------------------------------
 * 5. INDEPENDENT REAL-DOMAIN REPLICATION
 * ------------------------------------------------------------
 */

const crossDomain =
  report?.cross_domain_replication || {};

const crossDomainStd =
  Number(
    crossDomain.real_domain_std
  );

const independentDomains =
  Number(
    crossDomain
      .independent_secondary_real_domains
      ?? 0
  );

assert(
  finite(crossDomainStd),
  "cross-domain standard deviation is not finite"
);

assert(
  crossDomainStd <=
    Number(expected.max_cross_domain_std),
  (
    `cross-domain std=${crossDomainStd} exceeds ` +
    `${expected.max_cross_domain_std}`
  )
);

assert(
  independentDomains >=
    Number(
      expected
        .min_independent_secondary_real_domains
    ),
  (
    `independent secondary domains=${independentDomains} ` +
    "below declared minimum"
  )
);

/*
 * ------------------------------------------------------------
 * 6. PRIMARY STOCHASTIC NULL
 *
 * This is the authoritative scientific support gate.
 *
 * Non-rejection is not a software defect.
 * It blocks scientific claim promotion.
 * ------------------------------------------------------------
 */

const stochasticNull =
  report?.appropriate_stochastic_null;

assert(
  stochasticNull &&
  typeof stochasticNull === "object",
  "appropriate_stochastic_null is missing"
);

assert(
  stochasticNull.valid === true,
  "primary stochastic null result is invalid"
);

assert(
  stochasticNull.support_eligible === true,
  "primary stochastic null is not support-eligible"
);

assert(
  stochasticNull.scientific_role ===
    "primary_stochastic_null_gate",
  "primary stochastic null has incorrect scientific role"
);

assert(
  stochasticNull.null_model ===
    "stationary_gaussian_ar_p_aic",
  "unexpected primary stochastic null model"
);

assert(
  stochasticNull.test_endpoint ===
    "canonical_primary_alpha",
  "primary stochastic null endpoint mismatch"
);

assert(
  stochasticNull.alternative ===
    "greater_than_null",
  "primary stochastic null alternative mismatch"
);

assert(
  stochasticNull.tail === "upper",
  "primary stochastic null tail mismatch"
);

assert(
  stochasticNull.permutation_null_is_primary ===
    false,
  "permutation null cannot be primary"
);

const pValue =
  Number(
    stochasticNull.p_value_mc_add_one
  );

assert(
  finite(pValue),
  "primary stochastic null p-value is not finite"
);

/*
 * IMPORTANT:
 * The current scientific state is expected to stop here.
 * That is correct.
 */

if (
  stochasticNull.reject_at_0_05 !== true
) {
  console.error(
    "❌ CLAIM PROMOTION BLOCKED"
  );

  console.error(
    "Primary stochastic null was not rejected."
  );

  console.error(
    `Primary stochastic-null p-value: ${pValue}`
  );

  console.error(
    "Scientific claim remains under investigation."
  );

  process.exit(1);
}

/*
 * ------------------------------------------------------------
 * 7. CLEAN-CHECKOUT COMPUTATIONAL REPRODUCIBILITY
 * ------------------------------------------------------------
 */

assert(
  exists(REPLAY_PATH),
  `missing ${REPLAY_PATH}`
);

const replay =
  readJson(REPLAY_PATH);

assert(
  replay &&
  typeof replay === "object",
  "external replay artifact is invalid"
);

assert(
  replay.clean_checkout_reproducibility_verified
    === true,
  "clean-checkout computational reproducibility is not verified"
);

assert(
  replay.fingerprint_match === true,
  "clean-checkout fingerprint does not match"
);

assert(
  replay.structure_match === true,
  "clean-checkout report structure does not match"
);

assert(
  replay.status === "verified",
  "external replay verification status is not verified"
);

assert(
  typeof replay.source_commit === "string" &&
  /^[0-9a-f]{40}$/i.test(
    replay.source_commit
  ),
  "external replay source_commit is not a valid full commit SHA"
);

if (
  process.env.GITHUB_SHA
) {
  assert(
    replay.source_commit.toLowerCase() ===
      process.env.GITHUB_SHA.toLowerCase(),
    "external replay source_commit does not match GITHUB_SHA"
  );
}

/*
 * ------------------------------------------------------------
 * 8. ADVERSARIAL CONTROL
 * ------------------------------------------------------------
 */

assert(
  exists(ADVERSARIAL_PATH),
  `missing ${ADVERSARIAL_PATH}`
);

const adversarial =
  readJson(ADVERSARIAL_PATH);

assert(
  adversarial &&
  typeof adversarial === "object",
  "adversarial control artifact is invalid"
);

assert(
  adversarial.passed === true,
  "adversarial control did not pass"
);

/*
 * ------------------------------------------------------------
 * 9. EXPLICIT EPISTEMIC SEPARATION
 * ------------------------------------------------------------
 */

assert(
  report?.scientific_interpretation
    ?.permutation_null_is_primary === false,
  "permutation null must remain diagnostic-only"
);

/*
 * ------------------------------------------------------------
 * 10. FINAL PROMOTION
 * ------------------------------------------------------------
 */

console.log(
  "============================================"
);

console.log(
  "SCIENTIFIC CLAIM PROMOTION ELIGIBLE"
);

console.log(
  "============================================"
);

console.log(
  `canonical alpha: ${alpha}`
);

console.log(
  `primary stochastic-null p-value: ${pValue}`
);

console.log(
  "primary stochastic null: REJECTED"
);

console.log(
  "clean-checkout reproducibility: VERIFIED"
);

console.log(
  "fingerprint match: TRUE"
);

console.log(
  "adversarial control: PASSED"
);

console.log(
  "permutation null: diagnostic-only"
);

console.log(
  "scale stability: diagnostic-only"
);

console.log(
  "Scientific claim promotion gate passed."
);
