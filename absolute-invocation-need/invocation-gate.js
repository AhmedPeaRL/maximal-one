import { currentPressure, resetPressure } from "./pressure-memory.js";

const INVOCATION_THRESHOLD = 7;

export function shouldInvoke() {
  if (currentPressure() >= INVOCATION_THRESHOLD) {
    resetPressure();
    return true;
  }
  return false;
}
