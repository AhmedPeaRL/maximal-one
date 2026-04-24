export function anchorTruth(payload, signature) {
  return {
    hash: signature,
    invariant: extractInvariant(payload),
    timestamp: Date.now(),
    entropy: measureEntropy(payload)
  };
}

function extractInvariant(p) {
  try {
    return JSON.stringify(p).length % 97;
  } catch {
    return 0;
  }
}

function measureEntropy(p) {
  const str = JSON.stringify(p);
  let e = 0;

  for (let i = 0; i < str.length; i++) {
    e += str.charCodeAt(i);
  }

  return e % 1000;
}
