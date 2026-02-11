/**
 * Artifact state.
 * No triggers.
 * No conditions.
 * Only allowance.
 */

export const artifactState = {
  lastManifestation: null,
  totalManifestations: 0
};

export function manifest(timestamp) {
  artifactState.lastManifestation = timestamp;
  artifactState.totalManifestations += 1;
}
