import fs from "fs";

const historyPath =
  "./core-scientific/publication-gate/validation-history.json";

const evolutionPath =
  "./core-scientific/publication-gate/evolution-log.json";

export function recordEvolution(commitHash, report) {
  let history = [];

  if (fs.existsSync(evolutionPath)) {
    history = JSON.parse(fs.readFileSync(evolutionPath));
  }

  const entry = {
    timestamp: Date.now(),
    commit: commitHash,
    mean: report.envelopeCheck.mean,
    variance: report.envelopeCheck.variance,
    relativeError: report.errorCheck.relativeError
  };

  history.push(entry);

  fs.writeFileSync(
    evolutionPath,
    JSON.stringify(history, null, 2)
  );

  let drift = null;

  if (history.length > 1) {
    const prev = history[history.length - 2];
    drift = {
      meanDrift: entry.mean - prev.mean,
      varianceDrift: entry.variance - prev.variance,
      errorDrift: entry.relativeError - prev.relativeError
    };
  }

  return {
    recorded: true,
    totalRuns: history.length,
    drift
  };
}
