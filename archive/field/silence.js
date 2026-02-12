// field/silence.js

export function shouldRemainSilent(parsed) {
  if (parsed.entropy < 5) return true;
  if (parsed.length < 12) return true;
  return Math.random() < 0.7; // الصمت هو الأصل
}
