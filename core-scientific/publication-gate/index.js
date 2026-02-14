import { enforceMeanError } from "./error-check.js";

function relativeError(empirical, theoretical) {
  return Math.abs(empirical - theoretical) / Math.abs(theoretical || 1);
}

export function publicationGate({
  empiricalMean,
  theoreticalMean,
  empiricalStd,
  sampleSize
}) {

  console.log("---- DIAGNOSTICS ----");
  console.log("Empirical Mean:", empiricalMean);
  console.log("Theoretical Mean:", theoreticalMean);
  console.log("Empirical Std:", empiricalStd);
  console.log("Sample Size:", sampleSize);

  const relError = relativeError(empiricalMean, theoreticalMean);
  console.log("Relative Error:", relError);

  if (empiricalStd === 0) {
    throw new Error("Variance is zero — system is degenerate.");
  }

  if (!Number.isFinite(empiricalMean)) {
    throw new Error("Numerical explosion detected.");
  }

  const meanCheck = enforceMeanError(
    empiricalMean,
    theoreticalMean,
    null,
    empiricalStd,
    sampleSize
  );

  if (relError > 0.01) {
    throw new Error(
      `Relative error exceeds 1% threshold: ${relError}`
    );
  }

  console.log("Publication Gate: PASSED");

  return {
    meanCheck,
    relativeError: relError,
    status: "READY_FOR_PUBLICATION"
  };
      }
