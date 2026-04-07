export async function handler(event) {
  try {
    const payload = JSON.parse(event.body || "{}");

    const response = await fetch(
      "https://api.github.com/repos/AhmedPeaRL/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          "Accept": "application/vnd.github+json",
          "Authorization": `Bearer ${process.env.GITHUB_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "external_witness",
          client_payload: payload
        })
      }
    );

    if (!response.ok) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: "GitHub dispatch failed" })
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ ok: true })
    };

  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
}
