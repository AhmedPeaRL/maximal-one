const fs = require("fs");
const path = require("path");

const bufferPath = path.join(__dirname, "..", "buffer", "cold.buffer.json");

function allowOnce() {
  const buf = JSON.parse(fs.readFileSync(bufferPath, "utf8"));
  const now = Date.now();

  if (buf.last_pass && now - buf.last_pass < 1000 * 60 * 60) {
    return false; // ساعة صمت إجباري
  }

  buf.last_pass = now;
  fs.writeFileSync(bufferPath, JSON.stringify(buf, null, 2));
  return true;
}

module.exports = { allowOnce };
