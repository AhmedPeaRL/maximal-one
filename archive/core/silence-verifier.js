import fs from "fs";

const SILENCE_THRESHOLD_SECONDS = 3600; // ساعة صمت حقيقي

export function verifySilence(lastInteractionTimestamp) {
  const now = Date.now();
  const duration = Math.floor((now - lastInteractionTimestamp) / 1000);

  if (duration >= SILENCE_THRESHOLD_SECONDS) {
    fs.appendFileSync(
      "ledger/silence.log",
      `${new Date().toISOString()} | ${duration} | verified\n`
    );
    return true;
  }

  return false;
}
