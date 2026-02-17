const { executeTransition } = require('./state-machine');
const fs = require('fs');
const path = require('path');

const CONTRACT_PATH = path.join(__dirname, 'external-input-contract.json');

function validateEvent(event) {
  const contract = JSON.parse(fs.readFileSync(CONTRACT_PATH));

  if (!contract.allowedEventTypes.includes(event.type)) {
    throw new Error('Event type not allowed.');
  }

  return true;
}

function processEvent(event) {
  validateEvent(event);
  const newStateHash = executeTransition(event);
  console.log('New Deterministic State Hash:', newStateHash);
  return newStateHash;
}

module.exports = {
  processEvent
};
