import { isPassageOpen, closePassage } from "./passage-state.js";

export function resolvePassage() {
  if (!isPassageOpen()) return null;

  closePassage();

  return {
    status: "passed",
    mode: "silent",
    timestamp: new Date().toISOString()
  };
}
