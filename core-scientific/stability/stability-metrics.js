const fs = require("fs");

function shannonEntropy(values) {
  const total = values.length;
  if (total === 0) return 0;

  const counts = {};
  values.forEach(v => {
    counts[v] = (counts[v] || 0) + 1;
  });

  return Object.values(counts).reduce((entropy, count) => {
    const p = count / total;
    return entropy - p * Math.log2(p);
  }, 0);
}

function transitionMatrix(values) {
  const matrix = {};
  for (let i = 1; i < values.length; i++) {
    const from = values[i - 1];
    const to = values[i];

    if (!matrix[from]) matrix[from] = {};
    matrix[from][to] = (matrix[from][to] || 0) + 1;
  }
  return matrix;
}

function driftCoefficient(values) {
  if (values.length < 2) return 0;

  let changes = 0;
  for (let i = 1; i < values.length; i++) {
    if (values[i] !== values[i - 1]) {
      changes++;
    }
  }

  return changes / (values.length - 1);
}

module.exports = {
  shannonEntropy,
  transitionMatrix,
  driftCoefficient
};
