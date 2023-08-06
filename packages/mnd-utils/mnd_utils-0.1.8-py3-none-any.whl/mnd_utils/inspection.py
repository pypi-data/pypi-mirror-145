import ast
import inspect


def number_callable_params(callable):
	"""
	Número de parámetros de una función o callable.
	:param callable: objeto que puede ser invocado
	:return:
	"""
	return len(inspect.signature(callable).parameters)


def function_has_return(callable):
	"""
	Devuelve True si la función tiene sentencia return, False en caso contrario.
	No funciona con funciones cuyo código no esté escrito en Python.
	:param callable:
	:return:
	"""
	return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(callable))))


def next_class_in_mro(instance_class: type, current_class: type) -> type:
	mro = instance_class.__mro__
	for i, clazz in enumerate(mro):
		if clazz == current_class:
			if i < len(mro) - 1:
				return mro[i + 1]
	return None


def exist_method_in_parent_classes(instance: object, current_class: type, method_name: str) -> bool:
	instance_class = instance.__class__
	mro = instance_class.__mro__
	for i, clazz in enumerate(mro):
		if clazz == current_class:
			next_classes = mro[i + 1:]
			for next_class in next_classes:
				if method_name in dir(next_class):
					return True
	return False
