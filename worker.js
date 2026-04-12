export default {
  async fetch(request) {
    if (request.method !== 'POST') {
      return new Response("Method not allowed", { status: 405 });
    }

    const body = await request.json();

    const res = await fetch("https://api.github.com/repos/AhmedPeaRL/maximal-one/dispatches", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${GH_TOKEN}`,
        "Accept": "application/vnd.github+json"
      },
      body: JSON.stringify({
        event_type: "external_witness",
        client_payload: body
      })
    });

    return new Response(JSON.stringify({ ok: res.ok }), {
      headers: { "Content-Type": "application/json" }
    });
  }
};
