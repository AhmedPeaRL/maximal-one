let last = null;

function sovereignGate() {
  const now = Date.now();
  if (last && now - last < 1000 * 60 * 60 * 12) return false; // 12 ساعة
  last = now;
  return true;
}

module.exports = { sovereignGate };
