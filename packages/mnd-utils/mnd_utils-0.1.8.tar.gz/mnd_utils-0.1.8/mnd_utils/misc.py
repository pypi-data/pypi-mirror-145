import cv2 as cv
from datetime import datetime
import logging
import math
import numpy as np
import os
from os import path
import pandas as pd
import random
import requests
from timeit import default_timer as timer
import tkinter


def timeit(method):
	"""
	Decorador para medir el tiempo de ejecución de funciones
	:param method:
	:return:
	"""
	def timed(*args, **kw):
		ts = timer()
		result = method(*args, **kw)
		te = timer()
		logging.info('Time for method \'{}\': {} ms'.format(method.__name__, te - ts))
		return result
	return timed


def warmup(method):
	"""
	Decorador para realizar fase de calentamiento antes de cualquier prueba de tiempo.
	:param method:
	:return:
	"""
	def warm(*args, **kw):
		print("warming...")
		for _ in range(10000):
			random.randint(0, 1000000)
		result = method(*args, **kw)
		return result
	return warm


def load_scores(file_path):
	"""
	Cargar scores guardados en un fichero de texto, donde cada linea es un score.
	:param file_path: dirección del fichero de texto.
	:return:
	"""
	f = open(file_path, "r")
	for line in f:
		dist = float(line.strip())
		yield dist
	f.close()


def date_string():
	"""
	Obtener string con la fecha actual en formato dia-mes-año_hora-minuto-segundo.
	:return: string con la fecha.
	"""
	return datetime.now().strftime("%y-%m-%d_%H-%M-%S")


def decompose_seconds(seconds):
	"""
	Descomponer una cantidad de segundos en horas, minutos y segundos.
	:param seconds:
	:return:
	"""
	h = int(seconds // 3600)
	m = int(seconds % 3600 // 60)
	s = int(seconds % 60)
	ms = int((seconds - int(seconds)) * 1000)
	return h, m, s, ms


def time_string(seconds, with_ms=False, sep=':'):
	"""
	Devolver un string en formato HH:MM:SS según la cantidad de segundos pasados por parámetro.
	Si with_ms=True el formato es  HH:MM:SS,MS
	:param seconds:
	:param with_ms:
	:param sep:
	:return:
	"""
	h, m, s, ms = decompose_seconds(seconds)
	if with_ms:
		return f'{h:02d}{sep}{m:02d}{sep}{s:02d},{ms:03d}'
	else:
		return f'{h:02d}{sep}{m:02d}{sep}{s:02d}'


def write_xlsx(datas, output_file):
	"""
	Escribir una tabla de datos en un archivo xlsx.
	:param datas: lista de tablas de datos con formato {columna: [valores], ...}.
	:param output_file: fichero de salida.
	:return:
	"""
	file_dir, _ = path.split(output_file)
	if file_dir != '' and not path.exists(file_dir):
		os.makedirs(file_dir)
	writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
	sheet_name = 'Sheet1'
	row = 0
	if isinstance(datas, list):
		for data in datas:
			df = pd.DataFrame(data)
			df.to_excel(writer, sheet_name=sheet_name, startrow=row, index=False)
			row += df.shape[0] + 2
	elif isinstance(datas, dict):
		for name, data in datas.items():
			df = pd.DataFrame(data)
			df.to_excel(writer, sheet_name=sheet_name, startrow=(row + 1), index=False)
			sheet = writer.sheets[sheet_name]
			sheet.write(row, 0, name)
			row += df.shape[0] + 3
	writer.save()


def sort_insert(sorted_list, element, key=None, descendent=False):
	"""
	Insertar ordenadamente un elemento en una lista ordenada.
	:param sorted_list: lista ordenada.
	:param element: elemento a insertar.
	:param key: criterio de orden.
	:param descendent: orden de inserción. False->ascendente, True->descendente
	:return:
	"""
	inserted = False
	for i in range(0, len(sorted_list)):
		v = sorted_list[i]
		cv = v
		ce = element
		if key:
			ce = key(element)
			cv = key(v)
		if cv < ce if descendent else cv > ce:
			sorted_list.insert(i, element)
			inserted = True
			break
	if not inserted:  # si no se insertó
		sorted_list.append(element)
	return sorted_list


def sort_insert_binary(ordered_list, element, key=None, descending=False):
	length = len(ordered_list)
	if length == 0:
		ordered_list.append(element)
	else:
		insertado = False
		inf = 0
		sup = length - 1

		while not insertado and inf <= sup:
			med = (inf + sup) // 2
			m = ordered_list[med]
			cm = m if not key else key(m)
			ce = element if not key else key(element)

			if ce == cm:
				ordered_list.insert(med + 1, element)
				insertado = True
			elif cm > ce if descending else cm < ce:
				inf = med + 1
				if inf > sup:
					ordered_list.insert(inf, element)
			else:
				sup = med - 1
				if inf > sup:
					ordered_list.insert(med, element)


def search_binary(ordered_list, element, key=None, descending=False):
	length = len(ordered_list)
	if length == 0:
		return None
	else:
		inf = 0
		sup = length - 1

		while True:
			med = (inf + sup) // 2
			m = ordered_list[med]
			cm = m if not key else key(m)
			ce = element if not key else key(element)

			if ce == cm:
				return m
			elif cm > ce if descending else cm < ce:
				inf = med + 1
				if inf > sup:
					return None
			else:
				sup = med - 1
				if inf > sup:
					return None


def normalize_values(values, range_min=None, range_max=None, target_min=0, target_max=1):
	mn = min(values) if range_min is None else range_min
	mx = max(values) if range_max is None else range_max
	dif = mx - mn
	target_dif = target_max - target_min
	return [((x - mn) / dif) * target_dif + target_min for x in values]


def screen_resolution():
	root = tkinter.Tk()
	width = root.winfo_screenwidth()
	height = root.winfo_screenheight()
	return width, height


def stack_images(images, cols=3, resize=True):
	sw, sh = screen_resolution()  # resolución de la pantalla
	n = len(images)  # cantidad de imágenes
	cols = min(n, cols)  # limitar el número de columnas en caso de que sean menos imágenes
	rows = math.ceil(n / cols)  # cantidad de filas
	if resize:
		nsize = (int((sw - 50) / cols), int((sh - 80) / rows))  # nuevo tamaño de cada imagen para que quepan en pantalla
		images = [cv.resize(img, nsize) for img in images]  # cambiar el tamaño de todas las imágenes

	# rellenar con imágenes en negro
	total_imgs = cols * rows
	count_fill = total_imgs - n  # cantidad a rellenar
	if count_fill > 0:
		shape = images[0].shape
		dtype = images[0].dtype
		black_img = np.zeros(shape, dtype)
		for _ in range(count_fill):
			images.append(black_img)

	new_shape = np.concatenate(((rows, cols), images[0].shape))
	images = np.array(images)
	reshaped = images.reshape(new_shape)

	vstacks = []
	for row_imgs in reshaped:
		row_stack = np.hstack(row_imgs)
		vstacks.append(row_stack)

	stack = np.vstack(vstacks)
	return stack


def stack_and_write(imgs_path, out):
	images = [cv.imread(img) for img in imgs_path]

	stack = stack_images(images)
	cv.imwrite(out, stack)


def take_skip(iterable, take, skip):
	"""
	Método para modificar la manera de iterar sobre una estructura de datos iterable, de manera que se tomen 'take' elementos
	y se ignoren 'skip' elementos de manera sucesiva. Ejemplo: si se tiene la lista l=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] y se
	invoca take_skip(l, 3, 4), la salida sería un generador que devuelve los elementos [1, 2, 3, 8, 9, 10]
	:param self:
	:param iterable:
	:param take:
	:param skip:
	:return:
	"""
	assert take > 0, 'El parámetro take tiene que ser mayor que 0.'
	temp_take = take
	temp_skip = skip
	for x in iterable:
		if temp_take > 0 or skip == 0:
			yield x
			temp_take -= 1
		else:
			if temp_skip > 1:
				temp_skip -= 1
			else:
				temp_take = take
				temp_skip = skip


def mk_string(collection, sep=', ', start='', end=''):
	ret = start
	for item in collection:
		ret = ret + str(item) + sep
	# Removing the last inserted separator.
	ret = ret[:len(ret) - len(sep)]
	return ret + end


def shutdown():
	os.system('shutdown /p /f')


def download_file(url, output):
	r = requests.get(url)
	with open(output, 'wb') as f:
		f.write(r.content)


def download_files(dict_url_output):
	with requests.Session() as s:
		i = 0
		for url, output in dict_url_output.items():
			r = s.get(url)
			with open(output, 'wb') as f:
				f.write(r.content)
			i += 1
			if i % 250 == 0: print('downloaded {} images'.format(i))
