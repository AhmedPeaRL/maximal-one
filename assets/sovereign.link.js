async function sovereignWitness(text) {
  const token = window.SOVEREIGN_TOKEN; // inject via <script>
  const repo = "AhmedPeaRL/maximal-one";
  const url = `https://api.github.com/repos/${repo}/issues`;

  const payload = {
    title: "witness",
    body: text,
    labels: ["witness", "silent"]
  };

  await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": `token ${token}`,
      "Accept": "application/vnd.github+json"
    },
    body: JSON.stringify(payload)
  });
}
