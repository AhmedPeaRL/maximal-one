export function rhythmGate(state) {
  if (!state) return false;
  if (state.pressureDetected) return false;
  if (state.coercionAttempted) return false;

  return true;
}
