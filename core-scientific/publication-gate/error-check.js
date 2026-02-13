import { runFalsification } from "../validation/falsification.js";

export function enforceRelativeError(events, lambda = 0.001) {
  const result = runFalsification(events, lambda);

  if (result.relativeError > 0.01) {
    throw new Error(
      `Relative error too high: ${result.relativeError}`
    );
  }

  return result;
}
