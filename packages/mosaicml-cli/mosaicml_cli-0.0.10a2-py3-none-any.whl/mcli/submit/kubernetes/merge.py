""" K8s Merge for Recursive Dictionaries """
from functools import reduce


# NOTE: Replace with shared merge functionality.
def _merge(a, b, path=None):
    """
    Merges dictionaries and lists recursively. List items are merged if either equal, or
    are has objects with the same `name` field.
    """
    if path is None:
        path = []
    if isinstance(a, dict) and isinstance(b, dict):
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    _merge(a[key], b[key], path + [str(key)])
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    _merge(a[key], b[key], path + [str(key)])
                elif b[key] is None and a[key] is not None:
                    pass
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
    elif isinstance(a, list) and isinstance(b, list):
        for index, value in enumerate(b):
            # Strategy for merging list items. If they are equal, override.
            found = [
                x for x in a if ((isinstance(x, dict) and isinstance(value, dict)) and
                                 (x.get('name') == value.get('name')) or x == value)
            ]
            if len(found) > 0:
                if isinstance(a[index], dict) and isinstance(b[index], dict):
                    _merge(a[index], b[index], path + [str(index)])
                elif isinstance(a[index], list) and isinstance(b[index], list):
                    _merge(a[index], b[index], path + [str(index)])
                elif b[index] is None and a[index] is not None:
                    pass
                else:
                    a[index] = b[index]
            else:
                a.append(b[index])

    return a


def merge(base, other):
    return reduce(_merge, [base, other])
