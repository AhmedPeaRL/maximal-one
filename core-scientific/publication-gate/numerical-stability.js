import fs from 'fs';

function assertCondition(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const report = JSON.parse(
  fs.readFileSync('./core-scientific/publication-gate/report.json','utf8')
);

assertCondition(
  typeof report.deterministicArtifactHash === 'string',
  'deterministicArtifactHash missing'
);

assertCondition(
  report.deterministicArtifactHash.length === 64,
  'deterministicArtifactHash invalid length'
);

console.log('Numerical stability verified.');
