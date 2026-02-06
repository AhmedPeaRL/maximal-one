import { currentKnock, resetKnock } from "./knock-memory.js";

const KNOCK_THRESHOLD = 9;

export function allowEntry() {
  if (currentKnock() >= KNOCK_THRESHOLD) {
    resetKnock();
    return true;
  }
  return false;
}
