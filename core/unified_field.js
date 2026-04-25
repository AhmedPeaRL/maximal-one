// unified_field.js
// Stable deterministic binding layer

import { resolveState } from './state_resolver.js';
import { bindSystemLayers } from './system_binding.js';

export async function unifiedField(input) {
  const state = await resolveState();

  const base = {
    input,
    layer: state.layer || "unknown",
    field: state.field || "unstable"
  };

  const signature = await generateSignature(input, base);

  const field = {
    ...base,
    timestamp: Date.now(),
    signature
  };

  const bound = bindSystemLayers(input, field.layer, input.length);

  field.event = synthesizeEvent(field, bound);

  return field;
}

// deterministic hashing
async function generateSignature(input, state) {
  const encoder = new TextEncoder();
  const data = encoder.encode(input + JSON.stringify(state));

  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// event generator
function synthesizeEvent(field, bound) {
  const base = field.signature.slice(0, 8);

  return {
    state: field.field,
    score: parseInt(base, 16) % 1000,
    signature: field.signature,
    event: JSON.stringify(bound, null, 2)
  };
}
