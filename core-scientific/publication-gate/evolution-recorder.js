import fs from "fs";

const historyPath =
  "./core-scientific/publication-gate/validation-history.json";

export function recordEvolution(commitHash, report) {
  let history = [];

  if (fs.existsSync(historyPath)) {
    history = JSON.parse(
      fs.readFileSync(historyPath)
    );
  }

  const entry = {
    commit: commitHash,
    timestamp: new Date().toISOString(),
    mean: report.envelopeCheck.mean,
    variance: report.envelopeCheck.variance,
    relativeError: report.errorCheck.relativeError,
    confidence95: report.confidenceCheck.confidence95
  };

  history.push(entry);

  fs.writeFileSync(
    historyPath,
    JSON.stringify(history, null, 2)
  );

  // ---- Degradation Gate ----
  if (history.length > 3) {
    const avgError =
      history
        .slice(0, -1)
        .reduce((acc, h) => acc + h.relativeError, 0)
      / (history.length - 1);

    if (entry.relativeError > avgError * 1.5) {
      throw new Error(
        `Degradation detected: ${entry.relativeError} > ${avgError * 1.5}`
      );
    }
  }

  return { recorded: true, totalRuns: history.length };
}
