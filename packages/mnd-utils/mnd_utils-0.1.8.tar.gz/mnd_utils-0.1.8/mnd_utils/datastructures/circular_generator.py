import itertools


class CircularGenerator:
    """
    Circular generator to iterate over a generator infinitely.
    You must control the iteration to avoid an endless loop that locks your app.
    """

    def __init__(self, generator_provider: {}):
        self._generator_provider = generator_provider
        self._current_generator = generator_provider()

    def _reset(self):
        self._current_generator = self._generator_provider()

    def __next__(self):
        try:
            return self._current_generator.__next__()
        except StopIteration:
            self._reset()
            return self._current_generator.__next__()

    def __iter__(self):
        return self

    def __getitem__(self, item):
        if isinstance(item, slice):
            item: slice = item
            return itertools.islice(self, item.start, item.stop, item.step)
        elif isinstance(item, int):
            return itertools.islice(self, item, item + 1, 1)


if __name__ == '__main__':
    def provider():
        for i in [1, 2, 3]:
            yield i
    cg = CircularGenerator(provider)
    for x in cg[:5]:
        print(x)
    print(len(list(cg[:10])))
