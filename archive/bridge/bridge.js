const rules = require("./bridge.rules.json");
const { process } = require("../processor/process_once");

function shouldPass(input, lastPassTime) {
  if (!input || input.content.length < rules.min_content_length) return false;

  const now = Date.now();
  if (lastPassTime && (now - lastPassTime) < rules.cooldown_minutes * 60000)
    return false;

  return Math.random() < rules.pass_probability;
}

function bridge(input, lastPassTime) {
  if (!shouldPass(input, lastPassTime)) return null;
  return process(input);
}

module.exports = { bridge };
