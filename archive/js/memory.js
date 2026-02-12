export function remember(intensity) {
  const record = {
    at: Date.now(),
    intensity
  };
  console.log("residual:", record);
  return record;
}
