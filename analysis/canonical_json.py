import json
from analysis.deep_freeze import deep_freeze


def canonicalize(obj):

    obj = deep_freeze(obj, digits=8)

    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )


def write_canonical(path, obj):

    with open(path, "w", encoding="utf-8") as f:

        f.write(canonicalize(obj))
