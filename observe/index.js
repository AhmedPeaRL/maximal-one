export function observe(mutation) {
  if (!mutation) return null;

  return {
    observable: true,
    footprint: mutation,
    visibility: "public"
  };
}
