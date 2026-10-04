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
  fs.mkdirSync(
    "artifacts",
    { recursive: true }
  );

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
    promotion_allowed: false,
    scientific_role:
      "scientific_contract_evaluation",
    reason: message
  };

  writeEvaluation(result);

  console.error(
    `❌ SCIENTIFIC PIPELINE INVALID: ${message}`
  );

  process.exit(1);
}

const report =
  readJson(
    "artifacts/canonical_report.json"
  );

const claim =
  readJson(
    "core-scientific/strict_claim.json"
  );

if (
  !report ||
  typeof report !== "object"
) {
  invalid(
    "canonical_report.json is not an object"
  );
}

if (
  !claim ||
  typeof claim !== "object"
) {
  invalid(
    "strict_claim.json is not an object"
  );
}

const nullCalibrationPath =
  "artifacts/null_calibration_gate.json";

const replicationGatePath =
  "artifacts/independent_domain_replication_gate.json";

const nullCalibration =
  fs.existsSync(nullCalibrationPath)
    ? readJson(nullCalibrationPath)
    : null;

const replicationGate =
  fs.existsSync(replicationGatePath)
    ? readJson(replicationGatePath)
    : null;

const expected =
  claim.expected_result;

if (
  !expected ||
  typeof expected !== "object"
) {
  invalid(
    "strict_claim.json expected_result is missing"
  );
}

const alpha =
  Number(
    report?.spectral_profile
      ?.estimated_alpha
  );

const sigma =
  Number(
    report?.spectral_profile
      ?.bootstrap_std
  );

const methodDelta =
  Number(
    report?.cross_method_validation
      ?.agreement_delta
  );

const bootstrapDiscrepancy =
  Number(
    report?.bootstrap_center_discrepancy
      ?.std_units
  );

const crossDomain =
  report?.cross_domain_replication ||
  {};

const crossDomainStd =
  Number(
    crossDomain.real_domain_std
  );

const measurementValidSecondaryDomains =
  Number(
    crossDomain
      .measurement_valid_secondary_real_domains
      ?? 0
  );

const replicationEligibleSecondaryDomains =
  Number(
    crossDomain
      .replication_eligible_secondary_real_domains
      ?? 0
  );

const stochasticNull =
  report?.appropriate_stochastic_null;

if (
  !stochasticNull ||
  typeof stochasticNull !== "object"
) {
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
    sigma <=
      Number(
        expected.max_sigma
      ),

  method_agreement:
    finite(methodDelta) &&
    methodDelta <=
      Number(
        expected.max_method_delta
      ),

  bootstrap_consistency:
    finite(bootstrapDiscrepancy) &&
    bootstrapDiscrepancy <=
      Number(
        expected
          .max_bootstrap_center_discrepancy_sigma
      ),

  cross_domain_replication:
    finite(crossDomainStd) &&
    crossDomainStd <=
      Number(
        expected.max_cross_domain_std
      ),

  independent_secondary_domains:
    replicationEligibleSecondaryDomains >=
      Number(
        expected
          .min_independent_secondary_real_domains
      ),

  stochastic_null_valid:
    stochasticNull.valid === true,

  stochastic_null_support_eligible:
    stochasticNull.support_eligible === true,

  stochastic_null_rejected:
    stochasticNull.reject_at_0_05 === true
};

checks.null_calibration =
  nullCalibration !== null &&
  nullCalibration.status ===
    "CALIBRATION_NOT_REJECTED";

checks.independent_domain_replication =
  replicationGate !== null &&
  replicationGate.status ===
    "REPLICATION_ESTABLISHED";

const structuralChecksPassed =
  checks.alpha_range &&
  checks.sigma &&
  checks.method_agreement &&
  checks.bootstrap_consistency &&
  checks.cross_domain_replication &&
  checks.independent_secondary_domains &&
  checks.stochastic_null_valid &&
  checks.stochastic_null_support_eligible &&
  checks.null_calibration &&
  checks.independent_domain_replication;

const scientificClaimSupported =
  structuralChecksPassed &&
  checks.stochastic_null_rejected;

/*
 * ------------------------------------------------------------
 * Claim-level evidence
 *
 * These artifacts are deliberately NOT required for the
 * scientific contract to describe the current scientific
 * result. They ARE required for final promotion.
 * ------------------------------------------------------------
 */

const replayPath =
  "artifacts/external_replay_verification.json";

const adversarialPath =
  "artifacts/adversarial_control.json";

const replayExists =
  fs.existsSync(replayPath);

const adversarialExists =
  fs.existsSync(adversarialPath);

let replay = null;
let adversarial = null;

if (replayExists) {
  try {
    replay =
      readJson(replayPath);
  } catch (_) {
    replay = null;
  }
}

if (adversarialExists) {
  try {
    adversarial =
      readJson(adversarialPath);
  } catch (_) {
    adversarial = null;
  }
}

const reproducibilityVerified =
  replay?.clean_checkout_reproducibility_verified
    === true &&
  replay?.fingerprint_match === true &&
  replay?.structure_match === true &&
  replay?.status === "verified";

const adversarialPassed =
  adversarial?.passed === true;

const sourceCommitMatches =
  typeof process.env.GITHUB_SHA !== "string" ||
  (
    typeof replay?.source_commit === "string" &&
    replay.source_commit.toLowerCase() ===
      process.env.GITHUB_SHA.toLowerCase()
  );

const promotionPrerequisites = {
  scientific_claim_supported:
    scientificClaimSupported,

  clean_checkout_reproducibility_verified:
    reproducibilityVerified,

  adversarial_control_passed:
    adversarialPassed,

  replay_source_commit_matches:
    sourceCommitMatches
};

const promotionAllowed =
  Object.values(
    promotionPrerequisites
  ).every(Boolean);

const status =
  scientificClaimSupported
    ? "SCIENTIFIC_CLAIM_SUPPORTED_BY_DECLARED_GATE"
    : "UNDER_INVESTIGATION";

const result = {
  status,

  claim_support:
    Boolean(
      scientificClaimSupported
    ),

  promotion_allowed:
    Boolean(
      promotionAllowed
    ),

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
      Boolean(
        stochasticNull.valid
      ),

    support_eligible:
      Boolean(
        stochasticNull
          .support_eligible
      ),

    rejected:
      Boolean(
        stochasticNull
          .reject_at_0_05
      ),

    p_value_mc_add_one:
      finite(
        Number(
          stochasticNull
            .p_value_mc_add_one
        )
      )
        ? Number(
            stochasticNull
              .p_value_mc_add_one
          )
        : null,

    selected_order:
      stochasticNull.selected_order ??
      null,

    selected_order_max:
      stochasticNull.selected_order_max ??
      null,

    surrogate_boundary_fraction:
      stochasticNull
        ?.order_selection_diagnostic
        ?.surrogate_boundary_fraction ??
      null
  },

  promotionPrerequisites,

  external_replay_artifact_present:
    replayExists,

  adversarial_control_artifact_present:
    adversarialExists,

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

  measurement_valid_secondary_domains:
    measurementValidSecondaryDomains,

  replication_eligible_secondary_domains:
    replicationEligibleSecondaryDomains,

  independent_secondary_domains:
    replicationEligibleSecondaryDomains,

  interpretation:
    scientificClaimSupported
      ? (
          promotionAllowed
            ? "The declared scientific support conditions and claim-level reproducibility/adversarial prerequisites passed."
            : "The declared scientific support conditions passed, but final claim promotion remains blocked until all claim-level reproducibility and adversarial prerequisites pass."
        )
      : "The computational validation pipeline is valid, but the scientific claim remains under investigation because one or more declared support conditions are not satisfied."
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
  result.primary_null
    .p_value_mc_add_one
);

console.log(
  "Clean-checkout reproducibility verified:",
  reproducibilityVerified
);

console.log(
  "Adversarial control passed:",
  adversarialPassed
);

console.log(
  "Final promotion allowed:",
  promotionAllowed
);

console.log(
  "Permutation null remains diagnostic-only."
);

console.log(
  "Scientific contract evaluation completed."
);
