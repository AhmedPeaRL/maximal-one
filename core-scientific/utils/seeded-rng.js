export function createSeededRandom(seed = 123456) {
  let state = seed % 2147483647;
  if (state <= 0) state += 2147483646;

  return function () {
    state = (state * 16807) % 2147483647;
    return (state - 1) / 2147483646;
  };
}
