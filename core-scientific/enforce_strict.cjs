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
    `❌ STRICT CLAIM PROMOTION FAILURE: ${message}`
  );
  process.exit(1);
}

function require(condition, message) {
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

require(
  exists(REPORT_PATH),
  `missing ${REPORT_PATH}`
);

require(
  exists(CLAIM_PATH),
  `missing ${CLAIM_PATH}`
);

require(
  exists(REPLAY_PATH),
  (
    "missing external reproducibility evidence: " +
    REPLAY_PATH
  )
);

require(
  exists(ADVERSARIAL_PATH),
  (
    "missing adversarial control evidence: " +
    ADVERSARIAL_PATH
  )
);

const report = readJson(
  REPORT_PATH
);

const claim = readJson(
  CLAIM_PATH
);

const replay = readJson(
  REPLAY_PATH
);

const adversarial = readJson(
  ADVERSARIAL_PATH
);

const expected =
  claim.expected_result;

require(
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

require(
  finite(alpha),
  `canonical alpha is not finite: ${alpha}`
);

require(
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

require(
  finite(sigma),
  `bootstrap sigma is not finite: ${sigma}`
);

require(
  sigma <=
    Number(expected.max_sigma),
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
    report?.cross_method_validation?.agreement_delta
  );

require(
  finite(methodDelta),
  "cross-method delta is not finite"
);

require(
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
    report?.bootstrap_center_discrepancy?.std_units
  );

require(
  finite(bootstrapDiscrepancy),
  "bootstrap center discrepancy is not finite"
);

require(
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
    crossDomain.independent_secondary_real_domains
    ?? 0
  );

require(
  finite(crossDomainStd),
  "cross-domain standard deviation is not finite"
);

require(
  crossDomainStd <=
    Number(expected.max_cross_domain_std),
  (
    `cross-domain std=${crossDomainStd} exceeds ` +
    `${expected.max_cross_domain_std}`
  )
);

require(
  independentDomains >=
    Number(
      expected.min_independent_secondary_real_domains
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
 * Non-rejection is not a pipeline error.
 * It is a reason that claim promotion is blocked.
 * ------------------------------------------------------------
 */

const stochasticNull =
  report?.appropriate_stochastic_null;

require(
  stochasticNull &&
  typeof stochasticNull === "object",
  "appropriate_stochastic_null is missing"
);

require(
  stochasticNull.valid === true,
  "primary stochastic null result is invalid"
);

require(
  stochasticNull.support_eligible === true,
  "primary stochastic null is not support-eligible"
);

require(
  stochasticNull.scientific_role ===
    "primary_stochastic_null_gate",
  "primary stochastic null has incorrect scientific role"
);

require(
  stochasticNull.null_model ===
    "stationary_gaussian_ar_p_aic",
  "unexpected primary stochastic null model"
);

require(
  stochasticNull.test_endpoint ===
    "canonical_primary_alpha",
  "primary stochastic null endpoint mismatch"
);

require(
  stochasticNull.alternative ===
    "greater_than_null",
  "primary stochastic null alternative mismatch"
);

require(
  stochasticNull.tail === "upper",
  "primary stochastic null tail mismatch"
);

require(
  stochasticNull.permutation_null_is_primary ===
    false,
  "permutation null cannot be primary"
);

const stochasticNullPValue =
  Number(
    stochasticNull.p_value_mc_add_one
  );

require(
  finite(stochasticNullPValue),
  "primary stochastic null p-value is not finite"
);

const stochasticNullRejected =
  stochasticNull.reject_at_0_05 === true;

if (!stochasticNullRejected) {
  console.error(
    "❌ CLAIM PROMOTION BLOCKED"
  );

  console.error(
    "Primary stochastic null was not rejected."
  );

  console.error(
    `Primary stochastic-null p-value: ${stochasticNullPValue}`
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
 *
 * This evidence is intentionally external to canonical
 * report generation.
 *
 * Canonical generation must not consume prior replay evidence.
 * The promotion gate may consume the independently produced
 * replay artifact.
 * ------------------------------------------------------------
 */

require(
  replay &&
  typeof replay === "object",
  "external replay artifact is invalid"
);

require(
  replay.clean_checkout_reproducibility_verified === true,
  "clean-checkout computational reproducibility is not verified"
);

require(
  replay.fingerprint_match === true,
  "clean-checkout fingerprint does not match"
);

require(
  replay.structure_match === true,
  "clean-checkout report structure does not match"
);

require(
  replay.status === "verified",
  "external replay verification status is not verified"
);

require(
  typeof replay.source_commit === "string" &&
  /^[0-9a-f]{40}$/i.test(
    replay.source_commit
  ),
  "external replay source_commit is not a valid full commit SHA"
);

if (process.env.GITHUB_SHA) {
  require(
    replay.source_commit ===
      process.env.GITHUB_SHA,
    (
      "external replay source_commit does not "
      + "match GITHUB_SHA"
    )
  );
}

/*
 * ------------------------------------------------------------
 * 8. ADVERSARIAL CONTROL
 * ------------------------------------------------------------
 */

require(
  adversarial &&
  typeof adversarial === "object",
  "adversarial control artifact is invalid"
);

require(
  adversarial.passed === true,
  "adversarial control did not pass"
);

/*
 * ------------------------------------------------------------
 * 9. DIAGNOSTIC-ONLY SEPARATION
 * ------------------------------------------------------------
 *
 * These must never rescue a failed primary null.
 * At this point the primary null has already passed.
 * They are still explicitly excluded from the promotion
 * decision itself.
 * ------------------------------------------------------------
 */

require(
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
  `primary stochastic-null p-value: ${stochasticNullPValue}`
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
