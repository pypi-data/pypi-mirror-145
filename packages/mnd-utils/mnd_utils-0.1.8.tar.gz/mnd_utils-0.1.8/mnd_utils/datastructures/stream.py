from collections import Generator


class Stream:
	"""
	Estructura de datos para represantar un stream de datos que mantiene en memoria los elementos ya visitados.
	"""

	def __init__(self, generator: Generator):
		"""
		Constructor del stream. Recibe un generador que representa la fuente del stream
		:param generator:
		"""
		self._generator = generator
		self._data = []
		self.__last_index = 0
		self.__generator_ended = False

	def __getitem__(self, item):
		stop = item
		if isinstance(item, slice):
			stop = item.stop or -1
			if item.start is not None and item.start < 0:
				stop = -1

		if stop < 0:
			while not self.__generator_ended:
				self.__append_next_value()
		else:
			for i in range(self.__last_index, stop + 1):
				self.__append_next_value()

		return self._data[item]

	def __append_next_value(self):
		if not self.__generator_ended:
			try:
				nv = next(self._generator)
				self._data.append(nv)
				self.__last_index += 1
			except StopIteration:
				self.__generator_ended = True


if __name__ == '__main__':
	s = Stream(None)
	for x in s:
		print(x)
