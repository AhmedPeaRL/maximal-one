function plotPresence(events) {
  let ctx = document.getElementById("chart").getContext("2d");

  let labels = [];
  let values = [];

  let presence = 0;
  let lastTime = events[0]?.timestamp || 0;

  events.sort((a, b) => a.timestamp - b.timestamp);

  events.forEach(event => {
    const deltaSeconds = (event.timestamp - lastTime) / 1000;
    presence = presence * Math.exp(-0.001 * deltaSeconds) + event.weight;

    labels.push(new Date(event.timestamp).toLocaleTimeString());
    values.push(presence);

    lastTime = event.timestamp;
  });

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Presence Over Time",
        data: values
      }]
    }
  });
}
