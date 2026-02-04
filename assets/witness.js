async function witness(text) {
  const token = window.SOVEREIGN_TOKEN;
  if (!token) return;

  const repo = "AhmedPeaRL/maximal-one";
  const url = `https://api.github.com/repos/${repo}/issues`;

  const payload = {
    title: "witness",
    body: text,
    labels: ["witness", "silent"]
  };

  try {
    await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `token ${token}`,
        "Accept": "application/vnd.github+json"
      },
      body: JSON.stringify(payload)
    });
  } catch (_) {
    // silence is intentional
  }
}
