export function applyCausalFeedback(truth) {
  const body = document.body;
  const stateEl = document.getElementById("state");

  if (!truth || !truth.decision) return;

  const decision = truth.decision.global;

  // 🧠 visual binding to truth
  if (decision === "provisionally_valid") {
    body.style.background = "#071b0c"; // deep green
    stateEl.innerText = "coherent";
  }

  else if (decision === "rejected") {
    body.style.background = "#1b0707"; // deep red
    stateEl.innerText = "falsified";
  }

  else {
    body.style.background = "#0b0b0b"; // neutral
    stateEl.innerText = "uncertain";
  }

  // 🔁 subtle pulse
  body.animate(
    [
      { opacity: 0.95 },
      { opacity: 1 },
      { opacity: 0.95 }
    ],
    {
      duration: 1200,
      iterations: 1
    }
  );
}
