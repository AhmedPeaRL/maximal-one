function deepSort(obj) {
  if (Array.isArray(obj)) {
    return obj.map(deepSort);
  }

  if (obj && typeof obj === "object") {
    return Object.keys(obj)
      .sort()
      .reduce((acc, key) => {
        acc[key] = deepSort(obj[key]);
        return acc;
      }, {});
  }

  if (typeof obj === "number") {
    return Number(obj.toPrecision(15));
  }

  return obj;
}

function canonicalJSONStringify(obj) {
  return JSON.stringify(deepSort(obj));
}

module.exports = {
  canonicalJSONStringify
};
