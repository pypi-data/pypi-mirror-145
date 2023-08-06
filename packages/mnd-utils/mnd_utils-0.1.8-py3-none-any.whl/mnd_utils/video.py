import cv2 as cv
import numpy as np


def generate_test_video(frames=1000):
	"""
	Generador de imágenes donde cada imagen tiene el índice de su posición dibujado en el centro
	y codificado en el pixel superior izquierdo.
	Para decodificar el índice se debe usar lo siguiente:
		pixel = image[0][0]
		indice = pixel[0]*256**2 + pixel[1]*256 + pixel[2]
	:param frames: número de frames que se deseen generar.
	:return:
	"""
	shape = (64, 96, 3)
	for i in range(frames):
		img = np.zeros(shape)
		cv.putText(img, str(i), (32, 48), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
		# codificar en el pixel superior izquierdo el índice del frame
		img[0, 0] = (i // 256**2, (i % 256**2) // 256, i % 256)
		yield img.astype(np.uint8)


def parse_test_video_pixel(pixel):
	return pixel[0]*256**2 + pixel[1]*256 + pixel[2]


def write_video(output_dir, images, img_size, fps=20):
	out = cv.VideoWriter(output_dir, -1, fps, img_size)
	for img in images:
		out.write(img)
	out.release()


def get_format(video_path: str) -> tuple:
	cap = cv.VideoCapture(video_path)
	fourcc = int(cap.get(cv.CAP_PROP_FOURCC))
	c1, c2, c3, c4 = fourcc & 0xFF, fourcc & 0xFF00 >> 8, fourcc & 0xFF0000 >> 16, fourcc & 0xFF000000 >> 24
	cap.release()
	return c1, c2, c3, c4
