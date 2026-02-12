async function fetchAllWitnessEvents() {
  const response = await fetch(
    "https://api.github.com/repos/AhmedPeaRL/maximal-one/issues"
  );

  const issues = await response.json();

  return issues.map(issue => {
    const lines = issue.body.split("\n");

    const parsed = {};
    lines.forEach(line => {
      const [key, value] = line.split(":").map(s => s.trim());
      parsed[key] = value;
    });

    return {
      id: parsed.id,
      timestamp: Number(parsed.timestamp),
      weight: Number(parsed.weight),
      origin: parsed.origin
    };
  });
}

async function rebuildCanonicalState() {
  const events = await fetchAllWitnessEvents();
  return computeTemporalPresence(events);
}
