/**
 * This file does not trigger actions.
 * It only records that something was observed.
 */

export function observe(signal) {
  const snapshot = {
    observedAt: new Date().toISOString(),
    signal,
    acknowledged: true
  };

  return snapshot;
}
