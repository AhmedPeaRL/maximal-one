import { SYSTEM_STATE } from "./system-state.js";

export function runSystem() {
  return {
    state: SYSTEM_STATE,
    explanation: "System already in post-trigger state"
  };
}
