import sys
from itertools import chain


def total_size(o):
    seen = set()  # track which object id's have already been seen
    default_size = sys.getsizeof(0)  # estimate sizeof object without __sizeof__
    dict_handler = lambda d: chain.from_iterable(d.items())

    def sizeof(obj):
        if id(obj) in seen:  # do not double count the same object
            return 0
        seen.add(id(obj))
        s = sys.getsizeof(obj, default_size)

        if isinstance(obj, list):
            s += sum(map(sizeof, iter(obj)))
        if isinstance(obj, dict):
            s += sum(map(sizeof, dict_handler(obj)))
        return s

    return sizeof(o)


