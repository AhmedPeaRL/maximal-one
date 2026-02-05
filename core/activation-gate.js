import { verifySilence } from "./silence-verifier.js";

export function allowActivation(lastInteractionTimestamp) {
  const silenceVerified = verifySilence(lastInteractionTimestamp);

  if (!silenceVerified) {
    return {
      allowed: false,
      reason: "silence_not_verified"
    };
  }

  return {
    allowed: true,
    mode: "witness"
  };
}
