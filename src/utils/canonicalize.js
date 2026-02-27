function deepSortObject(obj) {
  if (Array.isArray(obj)) {
    return obj.map(deepSortObject);
  }

  if (obj !== null && typeof obj === "object") {
    const sorted = {};
    Object.keys(obj)
      .sort()
      .forEach((key) => {
        sorted[key] = deepSortObject(obj[key]);
      });
    return sorted;
  }

  if (typeof obj === "number") {
    // normalize floating precision explicitly
    return Number(obj.toPrecision(15));
  }

  return obj;
}

function canonicalJSONStringify(obj) {
  const normalized = deepSortObject(obj);
  return JSON.stringify(normalized);
}

module.exports = {
  canonicalJSONStringify,
};
