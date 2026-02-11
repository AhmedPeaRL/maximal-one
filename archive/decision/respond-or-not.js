import { distortionRisk } from "../shield/distortion-check.js";

export function shouldRespond(context) {
  if (distortionRisk(context)) return false;

  if (context.silenceCreatesFalsehood) return true;

  return false;
}
