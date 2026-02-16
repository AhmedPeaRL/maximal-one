import report from "./report.json" with { type: "json" };

function assertCondition(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

// Ensure deterministicArtifactHash exists
assertCondition(
  typeof report.deterministicArtifactHash === "string",
  "deterministicArtifactHash missing"
);

// Basic structural sanity check
assertCondition(
  report.deterministicArtifactHash.length === 64,
  "Invalid artifact hash length"
);

// Optional numeric guards (only if present)
if ("relativeError" in report) {
  assertCondition(
    typeof report.relativeError === "number",
    "relativeError invalid"
  );
}

if ("variance" in report) {
  assertCondition(
    typeof report.variance === "number",
    "variance invalid"
  );
}

console.log("Numerical stability verified.");
