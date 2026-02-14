import fs from "fs";

const snapshotPath =
  "./core-scientific/publication-gate/snapshot-baseline.json";

export function enforceSnapshot(currentState, seed) {
  if (!fs.existsSync(snapshotPath)) {
    fs.writeFileSync(
      snapshotPath,
      JSON.stringify(currentState, null, 2)
    );
    return { createdBaseline: true };
  }

  const baseline = JSON.parse(
    fs.readFileSync(snapshotPath)
  );

  const match =
    JSON.stringify(baseline) ===
    JSON.stringify(currentState);

  if (!match) {
    throw new Error(
      "Determinism violation: snapshot mismatch under fixed seed"
    );
  }

  return { snapshotMatch: true };
}
