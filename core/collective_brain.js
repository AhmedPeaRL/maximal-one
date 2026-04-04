import { witness } from "../core-scientific/kernel/witness.js";

export async function collectiveProcess(input) {
  const result = await witness(input);

  return {
    event: result?.event || null,
    raw: result
  };
}
