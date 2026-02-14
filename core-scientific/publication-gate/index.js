import fs from "fs";
import { enforceMeanError } from "./error-check.js";
import { runSensitivitySuite } from "../stability/sensitivity-test.js";
import { createSeededRNG } from "../utils/seeded-rng.js";

/* ============================= */
/* ===== Helper Functions ====== */
/* ============================= */

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function std(arr, m) {
  const variance =
    arr.reduce((sum, x) => sum + (x - m) ** 2, 0) /
    arr.length;
  return Math.sqrt(variance);
}

function relativeError(empirical, theoretical) {
  return Math.abs(empirical - theoretical) /
    Math.abs(theoretical || 1);
}

/* ============================= */
/* ===== Simulation Layer ====== */
/* ============================= */

function runSimulation(sampleSize = 10000) {
  const rng = createSeededRNG(42);
  const values = [];

  for (let i = 0; i < sampleSize; i++) {
    const x = rng() * 2 - 1;
    values.push(x);
  }

  return values;
}

/* ============================= */
/* ===== Publication Gate ====== */
/* ============================= */

function publicationGate({
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

  if (empiricalStd === 0) {
    throw new Error("Variance is zero — degenerate system.");
  }

  if (!Number.isFinite(empiricalMean)) {
    throw new Error("Numerical explosion detected.");
  }

  const relError = relativeError(
    empiricalMean,
    theoreticalMean
  );

  console.log("Relative Error:", relError);

  if (relError > 0.01) {
    throw new Error(
      `Relative error exceeds 1% threshold: ${relError}`
    );
  }

  const meanCheck = enforceMeanError(
    empiricalMean,
    theoreticalMean,
    null,
    empiricalStd,
    sampleSize
  );

  /* ========= Sensitivity ========= */

  const sensitivityResults = runSensitivitySuite();
  console.log("Sensitivity Suite:", sensitivityResults);

  /* ========= Report ========= */

  const report = {
    empiricalMean,
    theoreticalMean,
    empiricalStd,
    sampleSize,
    relativeError: relError,
    meanCheck,
    sensitivityResults,
    status: "READY_FOR_PUBLICATION"
  };

  fs.writeFileSync(
    "./core-scientific/publication-gate/report.json",
    JSON.stringify(report, null, 2)
  );

  console.log("Publication Gate: PASSED");
}

/* ============================= */
/* ========= EXECUTE =========== */
/* ============================= */

const sampleSize = 10000;
const theoreticalMean = 0;

const data = runSimulation(sampleSize);
const empiricalMean = mean(data);
const empiricalStd = std(data, empiricalMean);

publicationGate({
  empiricalMean,
  theoreticalMean,
  empiricalStd,
  sampleSize
});
