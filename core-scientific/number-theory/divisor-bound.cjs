// Deterministic divisor function and bound verification

function divisorCount(n) {
  let count = 0;
  for (let i = 1; i * i <= n; i++) {
    if (n % i === 0) {
      count += (i * i === n) ? 1 : 2;
    }
  }
  return count;
}

function verifyBound(limit = 10000) {
  for (let k = 1; k <= limit; k++) {
    const d = divisorCount(k);
    if (d > 2 * Math.sqrt(k)) {
      return {
        passed: false,
        failingK: k,
        d,
        bound: 2 * Math.sqrt(k)
      };
    }
  }

  return {
    passed: true,
    limit
  };
}

if (require.main === module) {
  const result = verifyBound(20000);
  console.log(JSON.stringify(result));
}

module.exports = { divisorCount, verifyBound };
