// external_truth_anchor.js
// binds truth to irreversible external hash

export async function externalTruthAnchor(result) {
  const encoder = new TextEncoder();
  const data = encoder.encode(JSON.stringify(result));

  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  const hash = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

  // bind to public time source
  const timestamp = new Date().toISOString();

  return {
    hash,
    timestamp,
    anchor: `HCM-${hash.slice(0, 16)}`
  };
}
