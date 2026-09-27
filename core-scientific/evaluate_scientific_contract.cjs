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

function writeEvaluation(result) {
  fs.mkdirSync("artifacts", {
    recursive: true
  });

  fs.writeFileSync(
    "artifacts/scientific_contract_evaluation.json",
    JSON.stringify(result, null, 2) + "\n",
    "utf8"
  );
}

function invalid(message) {
  const result = {
    status: "INVALID_PIPELINE",
    claim_support: false,
    scientific_role:
      "scientific_contract_evaluation",
    reason: message,
    promotion_allowed: false
  };

  writeEvaluation(result);

  console.error(
    `❌ SCIENTIFIC PIPELINE INVALID: ${message}`
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

if (!report || typeof report !== "object") {
  invalid("canonical_report.json is not an object");
}

if (!claim || typeof claim !== "object") {
  invalid("strict_claim.json is not an object");
}

if (!expected || typeof expected !== "object") {
  invalid("strict_claim.json expected_result is missing");
}

const alpha = Number(
  report?.spectral_profile?.estimated_alpha
);

const sigma = Number(
  report?.spectral_profile?.bootstrap_std
);

const methodDelta = Number(
  report?.cross_method_validation?.agreement_delta
);

const bootstrapDiscrepancy = Number(
  report?.bootstrap_center_discrepancy?.std_units
);

const crossDomain =
  report?.cross_domain_replication || {};

const crossDomainStd = Number(
  crossDomain.real_domain_std
);

const independentDomains = Number(
  crossDomain.independent_secondary_real_domains ?? 0
);

const stochasticNull =
  report?.appropriate_stochastic_null;

if (!stochasticNull ||
    typeof stochasticNull !== "object") {
  invalid(
    "appropriate_stochastic_null result is missing"
  );
}

const [minAlpha, maxAlpha] =
  expected.alpha_range;

const checks = {
  alpha_range:
    finite(alpha) &&
    alpha >= minAlpha &&
    alpha <= maxAlpha,

  sigma:
    finite(sigma) &&
    sigma <= Number(expected.max_sigma),

  method_agreement:
    finite(methodDelta) &&
    methodDelta <=
      Number(expected.max_method_delta),

  bootstrap_consistency:
    finite(bootstrapDiscrepancy) &&
    bootstrapDiscrepancy <=
      Number(
        expected.max_bootstrap_center_discrepancy_sigma
      ),

  cross_domain_replication:
    finite(crossDomainStd) &&
    crossDomainStd <=
      Number(expected.max_cross_domain_std),

  independent_secondary_domains:
    independentDomains >=
      Number(
        expected.min_independent_secondary_real_domains
      ),

  stochastic_null_valid:
    stochasticNull.valid === true,

  stochastic_null_support_eligible:
    stochasticNull.support_eligible === true,

  stochastic_null_rejected:
    stochasticNull.reject_at_0_05 === true
};

const structuralChecksPassed =
  checks.alpha_range &&
  checks.sigma &&
  checks.method_agreement &&
  checks.bootstrap_consistency &&
  checks.cross_domain_replication &&
  checks.independent_secondary_domains &&
  checks.stochastic_null_valid &&
  checks.stochastic_null_support_eligible;

const scientificClaimSupported =
  structuralChecksPassed &&
  checks.stochastic_null_rejected;

const status =
  scientificClaimSupported
    ? "SCIENTIFIC_CLAIM_SUPPORTED_BY_DECLARED_GATE"
    : "UNDER_INVESTIGATION";

const result = {
  status,

  claim_support:
    Boolean(scientificClaimSupported),

  promotion_allowed:
    Boolean(scientificClaimSupported),

  scientific_role:
    "scientific_contract_evaluation",

  authoritative_primary_null:
    "appropriate_stochastic_null",

  permutation_null_is_primary:
    false,

  permutation_null_is_diagnostic_only:
    true,

  checks,

  primary_null: {
    valid:
      Boolean(stochasticNull.valid),

    support_eligible:
      Boolean(stochasticNull.support_eligible),

    rejected:
      Boolean(stochasticNull.reject_at_0_05),

    p_value_mc_add_one:
      finite(
        Number(
          stochasticNull.p_value_mc_add_one
        )
      )
        ? Number(
            stochasticNull.p_value_mc_add_one
          )
        : null,

    selected_order:
      stochasticNull.selected_order ?? null,

    selected_order_max:
      stochasticNull.selected_order_max ?? null,

    surrogate_boundary_fraction:
      stochasticNull
        ?.order_selection_diagnostic
        ?.surrogate_boundary_fraction ?? null
  },

  canonical_alpha:
    finite(alpha)
      ? alpha
      : null,

  bootstrap_sigma:
    finite(sigma)
      ? sigma
      : null,

  method_delta:
    finite(methodDelta)
      ? methodDelta
      : null,

  cross_domain_std:
    finite(crossDomainStd)
      ? crossDomainStd
      : null,

  independent_secondary_domains:
    independentDomains,

  interpretation:
    scientificClaimSupported
      ? "All declared support conditions evaluated by this contract passed. This result is eligible for the separate claim-promotion gate."
      : "The computational validation pipeline is valid, but the scientific claim remains under investigation because one or more declared support conditions, including potentially the primary stochastic null, are not satisfied."
};

writeEvaluation(result);

console.log(
  "=== SCIENTIFIC CONTRACT EVALUATION ==="
);

console.log(
  "Status:",
  status
);

console.log(
  "Claim support:",
  scientificClaimSupported
);

console.log(
  "Primary stochastic null rejected:",
  checks.stochastic_null_rejected
);

console.log(
  "Primary stochastic-null p-value:",
  result.primary_null.p_value_mc_add_one
);

console.log(
  "Permutation null remains diagnostic-only."
);

console.log(
  "Scientific pipeline evaluation completed."
);
