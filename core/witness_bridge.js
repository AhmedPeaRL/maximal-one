export async function sendWitness(value) {
try {
await fetch("https://api.github.com/repos/YOUR_USERNAME/maximal-one/dispatches", {
method: "POST",
headers: {
"Accept": "application/vnd.github+json",
"Authorization": "Bearer " + window.ENV_TOKEN,
},
body: JSON.stringify({
event_type: "maximal-one-witness",
client_payload: { input: value }
})
});
} catch (e) {
console.log("Witness dispatch failed silently.");
}
}
