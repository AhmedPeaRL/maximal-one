let pressure = 0;

export function registerSignal(signalWeight = 1) {
  pressure += signalWeight;
}

export function currentPressure() {
  return pressure;
}

export function resetPressure() {
  pressure = 0;
}
