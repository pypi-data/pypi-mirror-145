import cv2 as cv
import numpy as np


def fit_in_size(img, size):
	"""
	Cambiar el tamaño de la imagen rellenando con color negro para mantener la relación de aspecto.
	:param img:
	:param size:
	:return:
	"""
	h, w, d = img.shape
	width, height = size
	if height <= 4 or width <= 4:
		return img

	image_aspect = w / h
	size_aspect = width / height

	resized_img = np.zeros((height, width, d), dtype=img.dtype)
	if image_aspect > size_aspect:  # top/bottom stripes
		new_h = round(width / image_aspect)
		img_copy = cv.resize(img, (width, new_h), interpolation=cv.INTER_AREA)
		offset = height - new_h
		half_offset = offset // 2
		resized_img[half_offset: half_offset + new_h, :, :] = img_copy[:, :, :]
	else:  # left/right stripes
		new_w = round(height * image_aspect)
		img_copy = cv.resize(img, (new_w, height), interpolation=cv.INTER_AREA)
		offset = width - new_w
		half_offset = offset // 2
		resized_img[:, half_offset: half_offset + new_w, :] = img_copy
	return resized_img


def empty_gray_image():
	return np.zeros((8, 8, 3), dtype=np.uint8) + 127
