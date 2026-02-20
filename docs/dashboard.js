async function loadJSON(path) {
  const res = await fetch(path);
  return res.json();
}

function drawChart(scores, mean, stdDev) {
  const canvas = document.getElementById("chart");
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const padding = 40;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;

  const max = Math.max(...scores, mean + 3 * stdDev);
  const min = Math.min(...scores, mean - 3 * stdDev);

  function yScale(v) {
    return padding + height - ((v - min) / (max - min)) * height;
  }

  function xScale(i) {
    return padding + (i / (scores.length - 1)) * width;
  }

  // Draw mean band
  ctx.fillStyle = "rgba(56,139,253,0.2)";
  const upper = yScale(mean + stdDev);
  const lower = yScale(mean - stdDev);
  ctx.fillRect(padding, upper, width, lower - upper);

  // Draw mean line
  ctx.strokeStyle = "#58a6ff";
  ctx.beginPath();
  ctx.moveTo(padding, yScale(mean));
  ctx.lineTo(padding + width, yScale(mean));
  ctx.stroke();

  // Draw score line
  ctx.strokeStyle = "#3fb950";
  ctx.beginPath();
  scores.forEach((v, i) => {
    const x = xScale(i);
    const y = yScale(v);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
}

async function main() {
  const raw = await loadJSON("../core-scientific/attractor-field/raw-history.json");
  const state = await loadJSON("../core-scientific/attractor-field/statistical-state.json");

  const scores = raw.scores || [];
  const mean = state.mean || 0;
  const stdDev = state.count > 1 ? Math.sqrt(state.m2 / (state.count - 1)) : 0;

  drawChart(scores, mean, stdDev);

  const latest = scores[scores.length - 1];
  const zScore = stdDev > 0 ? (latest - mean) / stdDev : 0;
  const burnInComplete = state.count >= 5;
  const passed = burnInComplete ? Math.abs(zScore) <= 3 : true;

  const statusDiv = document.getElementById("status");
  statusDiv.innerHTML = `
    Count: ${state.count}<br>
    Mean: ${mean.toFixed(6)}<br>
    StdDev: ${stdDev.toFixed(6)}<br>
    Z-Score: ${zScore.toFixed(6)}<br>
    Burn-in complete: ${burnInComplete}<br>
    Decision: <span class="${passed ? "good" : "bad"}">
      ${passed ? "ACCEPTED" : "REJECTED"}
    </span>
  `;
}

main();
