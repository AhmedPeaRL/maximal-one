export function logisticMap(r, x0, iterations = 1000, discard = 100) {
  let x = x0;
  const trajectory = [];

  for (let i = 0; i < iterations; i++) {
    x = r * x * (1 - x);

    if (i >= discard) {
      trajectory.push(x);
    }
  }

  return trajectory;
}
