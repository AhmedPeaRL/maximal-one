function witness() {
  const text = document.getElementById("invocation").value;
  if (!text.trim()) return;

  // No storage. No sending. No response.
  document.getElementById("ack").classList.remove("hidden");
}
