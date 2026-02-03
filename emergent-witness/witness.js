export function witness(observation) {
  if (!observation) return null;

  return {
    witnessed: true,
    snapshot: observation,
    hash: hash(JSON.stringify(observation))
  };
}

function hash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (h << 5) - h + str.charCodeAt(i);
    h |= 0;
  }
  return `w_${Math.abs(h)}`;
}
