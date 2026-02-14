export function runSensitivitySuite() {

  const seeds = [0.1, 0.11, 0.1001, 0.101];
  const r = 3.7;
  const iterations = 2000;
  const discard = 500;

  function logistic(x) {
    return r * x * (1 - x);
  }

  const results = [];

  for (const seed of seeds) {

    let x = seed;
    const trajectory = [];

    for (let i = 0; i < iterations; i++) {
      x = logistic(x);
      if (i >= discard) {
        trajectory.push(x);
      }
    }

    const mean = trajectory.reduce((a, b) => a + b, 0) / trajectory.length;

    results.push({
      seed,
      mean
    });
  }

  return results;
}
