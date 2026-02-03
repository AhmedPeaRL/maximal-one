/**
 * Residual state accumulator.
 * No interpretation. No inference.
 */

export const residualState = {
  totalEntries: 0,
  lastEntryAt: null,
  silenceDuration: null
};

export function registerEntry(timestamp) {
  residualState.totalEntries += 1;
  residualState.silenceDuration =
    residualState.lastEntryAt
      ? timestamp - residualState.lastEntryAt
      : null;

  residualState.lastEntryAt = timestamp;
}
