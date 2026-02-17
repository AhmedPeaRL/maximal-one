const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const REPORT_PATH = path.join(__dirname, '../publication-gate/report.json');

function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function computeSelfMetric() {
  const report = JSON.parse(fs.readFileSync(REPORT_PATH));
  
  const baseVector = [
    report.scientificHash,
    report.compositeSeal,
    report.deterministicArtifactHash
  ].join('');

  const metricHash = sha256(baseVector);

  const numericScore = parseInt(metricHash.slice(0, 12), 16);

  return {
    metricHash,
    numericScore
  };
}

module.exports = {
  computeSelfMetric
};
