const crypto = require('crypto');

function boundedEntropy(maxDrift = 0.0001) {
  const raw = crypto.randomBytes(32).toString('hex');
  const numeric = parseInt(raw.slice(0, 12), 16);
  const normalized = (numeric % 1000000) / 1000000;
  const bounded = normalized * maxDrift;
  return bounded;
}

module.exports = { boundedEntropy };
