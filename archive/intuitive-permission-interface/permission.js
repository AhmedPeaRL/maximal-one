async function checkPermission() {
  const input = document.getElementById("input").value;

  const response = await fetch("/api/allow", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input })
  });

  if (response.status === 204) {
    document.getElementById("output").innerText = "";
    return;
  }

  const text = await response.text();
  document.getElementById("output").innerText = text;
}
