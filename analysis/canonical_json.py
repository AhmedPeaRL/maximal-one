import json

from analysis.fixed_precision import (
    recursively_freeze
)


def canonicalize(obj):

    obj = recursively_freeze(obj)

    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )


def write_canonical(path, obj):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            canonicalize(obj)
    )
