export function recallTrace() {
  const traces = JSON.parse(localStorage.getItem("field-traces") || "[]");
  if (traces.length === 0) return;

  const last = traces[traces.length - 1];
  document.documentElement.style.setProperty(
    "--field-opacity",
    last.value
  );
}
