const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const REPORT_PATH = path.join(__dirname, '../publication-gate/report.json');
const MANIFEST_PATH = path.join(__dirname, '../publication-gate/state-manifest.json');
const TRANSITION_LOG = path.join(__dirname, 'transition-log.json');

function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function loadCurrentState() {
  const report = JSON.parse(fs.readFileSync(REPORT_PATH));
  return report.deterministicArtifactHash;
}

function loadManifest() {
  return JSON.parse(fs.readFileSync(MANIFEST_PATH));
}

function recordTransition(previousHash, newHash, event) {
  const entry = {
    timestamp: new Date().toISOString(),
    previousHash,
    newHash,
    event,
  };

  let log = [];
  if (fs.existsSync(TRANSITION_LOG)) {
    log = JSON.parse(fs.readFileSync(TRANSITION_LOG));
  }

  log.push(entry);
  fs.writeFileSync(TRANSITION_LOG, JSON.stringify(log, null, 2));
}

function deterministicTransform(input) {
  return sha256(input);
}

function executeTransition(eventPayload) {
  const currentHash = loadCurrentState();
  const manifest = loadManifest();

  if (currentHash !== manifest.deterministicArtifactHash) {
    throw new Error('State mismatch before transition.');
  }

  const inputString = JSON.stringify(eventPayload);
  const newHash = deterministicTransform(currentHash + inputString);

  recordTransition(currentHash, newHash, eventPayload);

  return newHash;
}

module.exports = {
  executeTransition
};
