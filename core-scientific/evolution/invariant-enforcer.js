const fs = require('fs');
const path = require('path');

const MANIFEST_PATH = path.join(__dirname, '../publication-gate/state-manifest.json');
const REPORT_PATH = path.join(__dirname, '../publication-gate/report.json');

function enforceInvariants() {
  const report = JSON.parse(fs.readFileSync(REPORT_PATH));
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH));

  if (report.deterministicArtifactHash !== manifest.deterministicArtifactHash) {
    throw new Error('Invariant violation: manifest mismatch.');
  }

  if (!report.scientificHash || !report.compositeSeal) {
    throw new Error('Invariant violation: missing core seals.');
  }

  return true;
}

module.exports = {
  enforceInvariants
};
