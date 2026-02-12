// field/parse.js

export function parseWitness(payload) {
  return {
    length: payload.content.length,
    entropy: new Set(payload.content).size,
    tone: payload.content.includes("?") ? "seeking" : "assertive",
    raw: payload,
  };
}
