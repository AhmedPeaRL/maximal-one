// Deterministic Monte Carlo using seeded PRNG

function mulberry32(seed) {
  return function () {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function randomEvents(count = 100, seed = 42) {
  const rng = mulberry32(seed);
  const values = [];

  for (let i = 0; i < count; i++) {
    const base = Math.exp(-0.01 * i);
    const noise = rng() * 0.001;
    values.push(base + noise);
  }

  return values;
}
