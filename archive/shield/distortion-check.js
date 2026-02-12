export function distortionRisk(context) {
  if (!context) return false;

  if (context.forcesResponse) return true;
  if (context.seeksValidation) return true;
  if (context.extractiveIntent) return true;

  return false;
}
