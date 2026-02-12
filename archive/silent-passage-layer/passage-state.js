let passageOpen = false;

export function openPassage() {
  passageOpen = true;
}

export function isPassageOpen() {
  return passageOpen;
}

export function closePassage() {
  passageOpen = false;
}
