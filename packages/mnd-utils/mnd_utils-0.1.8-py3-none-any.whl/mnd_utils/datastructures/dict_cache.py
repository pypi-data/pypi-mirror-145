

class DictCache:
    """
    Indexed cache data structure to keep data in memory for optimized accessing.
    Useful when you have a big volume of data, and you want to keep in memory a small subset of the most
    recent accessed elements in case you need them several times before loading another subset of data.
    Usage:

        cache = DictCache(cache_size=500)
        video_reader = <object to read frames of a video in disk>

        def get_frame_fast(frame_index):
            if cache.is_cached(frame_index):
                return cache[frame_index]  # fast access if accessed a second time before uncaching
            else:
                frame = video_reader.get_frame(frame_index)  # slow access first time
                cache.cache(frame_index, frame)
                return frame
    """

    def __init__(self, cache_size):
        self._cache_size = cache_size
        self._key_order_list = []
        self._cache_dict = {}

    def __getitem__(self, key):
        if self.is_cached(key):
            return self._cache_dict[key]
        else:
            raise KeyError(f"The specified key {key} is no cached")

    def is_cached(self, key) -> bool:
        return key in self._cache_dict

    def cache(self, key, value):
        if self.is_cached(key):
            self.uncache(key)

        self._key_order_list.append(key)
        self._cache_dict[key] = value

        self._handle_size()

    def uncache(self, key):
        if key in self._key_order_list:
            self._key_order_list.remove(key)
            self._cache_dict.pop(key)

    def clear_cache(self):
        while len(self._cache_dict) > 0:
            first_key = self._key_order_list[0]
            self.uncache(first_key)

    def _handle_size(self):
        while len(self._cache_dict) > self._cache_size:
            first_key = self._key_order_list[0]
            self.uncache(first_key)
