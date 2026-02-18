const fs = require('fs');
const crypto = require('crypto');

function attractorScore(path) {
  const data = fs.readFileSync(path);
  const hash = crypto.createHash('sha256').update(data).digest('hex');

  const numeric = parseInt(hash.slice(0, 16), 16);
  const score = (numeric % 1000000) / 1000000;

  return score;
}

if (require.main === module) {
  const score = attractorScore('./core-scientific/publication-gate/report.json');
  console.log('Attractor score:', score);
}

module.exports = { attractorScore };
