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

  history.push({
    commit: commitHash,
    timestamp: new Date().toISOString(),
    mean: report.envelopeCheck.mean,
    variance: report.envelopeCheck.variance,
    relativeError: report.errorCheck.relativeError,
    confidence95: report.confidenceCheck.confidence95
  });

  fs.writeFileSync(
    historyPath,
    JSON.stringify(history, null, 2)
  );

  return { recorded: true, totalRuns: history.length };
}
