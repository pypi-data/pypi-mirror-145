"""Misc/utils functions."""


def dict_deepmerge(a, b, path=None):
    """Merge b into a recursively."""

    if path is None:
        path = []

    for k in b:
        if k in a:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                dict_deepmerge(a[k], b[k], path + [str(k)])
            elif a[k] == b[k]:
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(k)]))
        else:
            a[k] = b[k]

    return a
