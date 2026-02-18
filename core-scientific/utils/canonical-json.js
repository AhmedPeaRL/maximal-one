function sortObject(obj) {
  if (Array.isArray(obj)) {
    return obj.map(sortObject);
  }

  if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj)
      .sort()
      .reduce((result, key) => {
        result[key] = sortObject(obj[key]);
        return result;
      }, {});
  }

  return obj;
}

function canonicalStringify(obj) {
  const sorted = sortObject(obj);
  return JSON.stringify(sorted);
}

module.exports = { canonicalStringify };
