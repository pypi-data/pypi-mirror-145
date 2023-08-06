class itemList:
    def __init__(self, items):
        """
        :meta private:"
        """
        self._items = items

    def __iter__(self):
        return iter(self._items)

    def get(self, k):
        """Fetch a specific item from the list"""
        for it in self._items:
            if it.name == k: return it
        raise ValueError('not found')


def _build_filter_kwargs(filters):
    norm = []
    for f in filters:
        if hasattr(f, '_filters'):
            norm.extend(f._filters)
        else:
            norm.append(f)

    filter_kwargs = {}
    for f in norm:
        if f.key in filter_kwargs:
            raise ValueError(f'duplicate {f.key} provided')
        filter_kwargs[f.key] = f.value

    return filter_kwargs


class queryFilter:
    def __init__(self, key, value):
        self.key = key
        self.value = value
