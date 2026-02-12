// field/respond.js

export function indirectResponse(parsed) {
  return {
    type: "reflection",
    seed: parsed.raw.content.slice(0, 12),
    timestamp: Date.now(),
  };
}
