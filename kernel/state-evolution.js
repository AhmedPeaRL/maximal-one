async function fetchWitnessEvents() {
  const response = await fetch(
    "https://api.github.com/repos/AhmedPeaRL/maximal-one/issues?state=all&per_page=50"
  );

  const issues = await response.json();

  return issues
    .filter(issue => issue.title === "witness")
    .map(issue => parseWitnessBody(issue.body));
}

function parseWitnessBody(body) {
  const lines = body.split("\n");

  let event = {};

  lines.forEach(line => {
    if (line.startsWith("timestamp:")) {
      event.timestamp = Number(line.replace("timestamp:", "").trim());
    }
    if (line.startsWith("weight:")) {
      event.weight = Number(line.replace("weight:", "").trim());
    }
  });

  return event;
}

async function recomputeStateFromWitness() {
  const events = await fetchWitnessEvents();

  let presence = 0;
  let residue = 0;

  events.forEach(event => {
    presence = presence * 0.98 + event.weight;
    residue += Math.log(1 + event.weight);
  });

  return {
    presence,
    residue,
    silence: presence < 25
  };
}
