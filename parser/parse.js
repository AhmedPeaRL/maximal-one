export function parse(signal) {
  return {
    length: signal.text.length,
    density: signal.text.split(" ").length,
    presence: true
  };
}
