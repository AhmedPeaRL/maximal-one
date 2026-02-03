export function observe(reaction) {
  if (!reaction) return null;

  return {
    presence: true,
    density: reaction.intensity,
    shape: reaction.mutation
  };
}
