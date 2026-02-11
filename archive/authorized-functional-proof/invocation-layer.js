import { CORE_STATE } from "./system-core.js";

export function invokeSystem() {
  return {
    state: CORE_STATE,
    invoked: true
  };
}
