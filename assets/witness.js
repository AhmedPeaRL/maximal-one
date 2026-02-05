// assets/witness.js

const FORM = document.getElementById("witness-form");
const INPUT = document.getElementById("witness-input");
const STATE = document.getElementById("state");

FORM.addEventListener("submit", async (e) => {
  e.preventDefault();

  const text = INPUT.value.trim();
  if (!text) return;

  STATE.innerText = "received";

  const payload = {
    content: text,
    timestamp: Date.now(),
    origin: "human",
  };

  await fetch("https://api.github.com/repos/AhmedPeaRL/maximal-one/dispatches", {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${window.SOVEREIGN_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      event_type: "witness-event",
      client_payload: payload,
    }),
  });

  INPUT.value = "";
  STATE.innerText = "witnessed";
});
