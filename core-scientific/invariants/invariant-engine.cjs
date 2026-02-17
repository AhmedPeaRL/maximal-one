function enforceInvariants(aggregated) {
  if (!Array.isArray(aggregated)) {
    throw new Error("Aggregated report must be an array.");
  }

  if (aggregated.length === 0) {
    throw new Error("Aggregated report is empty.");
  }

  const requiredFields = ["region", "deterministicArtifactHash"];

  aggregated.forEach((entry, index) => {
    requiredFields.forEach((field) => {
      if (!(field in entry)) {
        throw new Error(
          `Invariant violation: missing '${field}' in entry ${index}`
        );
      }
    });
  });

  console.log("Invariant layer: structure verified.");
}

module.exports = { enforceInvariants };
