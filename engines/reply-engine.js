export function considerExpression(state) {
  if (!state) return null;

  if (state.coherence !== true) return null;
  if (state.rhythmViolated === true) return null;

  // expression is allowed, not required
  return {
    expressed: false,
    reason: "silence preserved"
  };
}
