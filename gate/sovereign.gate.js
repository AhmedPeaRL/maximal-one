let last = null;

function sovereignGate() {
  const now = Date.now();
  if (last && now - last < 1000 * 60 * 60 * 12) return false; // 12 ساعة
  last = now;
  return true;
}

module.exports = { sovereignGate };

let lastAccepted = 0;
const WINDOW = 1000 * 60 * 60 * 24; // 24h

function allow() {
  const now = Date.now();
  if (now - lastAccepted < WINDOW) return false;
  lastAccepted = now;
  return true;
}

module.exports = { allow };
