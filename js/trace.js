export function trace(value) {
  const entry = {
    time: Date.now(),
    disturbance: value
  };
  console.debug("trace", entry);
  return entry;
}
