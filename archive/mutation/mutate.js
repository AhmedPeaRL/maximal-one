export function mutate(input) {
  const stamp = Date.now();

  if (typeof input === 'string') {
    return {
      type: 'string',
      length: input.length,
      entropy: uniqueChars(input),
      at: stamp
    };
  }

  if (typeof input === 'object') {
    return {
      type: 'object',
      keys: Object.keys(input).length,
      depth: depth(input),
      at: stamp
    };
  }

  return { type: 'unknown', at: stamp };
}

function uniqueChars(str) {
  return new Set(str).size;
}

function depth(obj, level = 1) {
  if (typeof obj !== 'object' || obj === null) return level;
  return Math.max(
    ...Object.values(obj).map(v => depth(v, level + 1)),
    level
  );
}
