export function observe(value) {
  const snapshot = {
    t: Date.now(),
    v: value
  };
  console.debug("field-observation", snapshot);
  return snapshot;
}
