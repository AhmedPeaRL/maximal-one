import { enforceRelativeError } from "./error-check.js";
import { enforceVariance } from "./variance-check.js";
import { detectExplosion } from "./stability-check.js";
import { randomEvents } from "../validation/montecarlo.js";

export function publicationGate() {
  const events = randomEvents(200, 999);

  const errorCheck = enforceRelativeError(events);
  const varianceCheck = enforceVariance();
  const stabilityCheck = detectExplosion(events);

  return {
    errorCheck,
    varianceCheck,
    stabilityCheck,
    status: "PASSED"
  };
}

// Allow direct execution
if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const result = publicationGate();
    console.log(result);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}
