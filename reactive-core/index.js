export function react(input) {
  if (!input || typeof input !== 'object') return null;

  const timestamp = new Date().toISOString();

  return {
    received: true,
    intensity: measure(input),
    mutation: mutate(input),
    at: timestamp
  };
}

function measure(input) {
  return Object.keys(input).length;
}

function mutate(input) {
  return Object.keys(input).reduce((acc, key) => {
    acc[key] = typeof input[key] === 'string'
      ? input[key].length
      : 1;
    return acc;
  }, {});
}
