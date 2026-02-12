let knockIntensity = 0;
let silenceDuration = 0;

export function registerSilence() {
  silenceDuration += 1;
  knockIntensity += silenceDuration * 0.3;
}

export function registerNoise() {
  knockIntensity -= 1;
  if (knockIntensity < 0) knockIntensity = 0;
}

export function currentKnock() {
  return knockIntensity;
}

export function resetKnock() {
  knockIntensity = 0;
  silenceDuration = 0;
}
