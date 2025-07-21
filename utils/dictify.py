from datetime import datetime, timedelta

_primitives = [str, int, float, bool, complex]

_collections = [list, set]


def dictify(v):
    if v is None:
        return None

    if type(v) in _primitives:
        return v

    if isinstance(v, datetime):
        return v.isoformat()

    if isinstance(v, timedelta):
        return v.total_seconds()

    if isinstance(v, dict):
        d = {}
        for key, val in v.items():
            if key == '_id' and ('id' not in v):  # Replace _id with id if not exists
                key = 'id'
            elif key[0:1] == '_':  # No internal property convertion
                continue
            d[key] = dictify(val)
        return d

    if type(v) == tuple:  # Think about 'return player, 201'
        return tuple(map(lambda e: dictify(e), v))

    if type(v) in _collections:
        return list(map(lambda e: dictify(e), v))

    to_dict = getattr(v, 'to_dict', None)
    if callable(to_dict):
        return dictify(to_dict())

    __dict__ = getattr(v, '__dict__', None)
    if __dict__ is not None:
        return dictify(__dict__)

    return str(v)