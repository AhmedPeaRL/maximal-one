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
    if (line.startsWith("id:")) {
      event.id = line.replace("id:", "").trim();
    } 
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
 return computeTemporalPresence(events);
}
