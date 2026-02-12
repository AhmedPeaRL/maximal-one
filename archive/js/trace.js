export function trace(value) {
  const entry = {
    time: Date.now(),
    disturbance: value
  };
  console.debug("trace", entry);
  return entry;
}

export function storeTrace(value) {
  const traces = JSON.parse(localStorage.getItem("field-traces") || "[]");

  traces.push({
    time: Date.now(),
    value
  });

  localStorage.setItem("field-traces", JSON.stringify(traces));
}
