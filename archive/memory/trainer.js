// memory/trainer.js

import fs from "fs";

export function extractTraining(memory) {
  return memory.map(e => ({
    input: e.raw.content,
    metadata: {
      entropy: e.entropy,
      tone: e.tone,
    }
  }));
}
