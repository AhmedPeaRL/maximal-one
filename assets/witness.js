document.getElementById("witness-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const input = document.getElementById("witness-input").value.trim();
  if (!input) return;

  const payload = {
    timestamp: new Date().toISOString(),
    signal: {
      text: input,
      presence: "acknowledged"
    }
  };

  await fetch("https://api.github.com/repos/AhmedPeaRL/maximal-one/actions/workflows/witness-proxy.yml/dispatches", {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": "Bearer " + window.PROXY_TRIGGER_TOKEN,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ref: "main",
      inputs: {
        payload: JSON.stringify(payload)
      }
    })
  });

  document.getElementById("witness-input").value = "";
});
