export function createSeededRandom(seed = 123456789) {
  let state = seed >>> 0;

  return function () {
    state = (1664525 * state + 1013904223) % 4294967296;
    return state / 4294967296;
  };
}
