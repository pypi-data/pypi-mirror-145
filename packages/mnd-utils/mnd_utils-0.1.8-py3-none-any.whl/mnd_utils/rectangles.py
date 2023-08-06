import numpy as np
import cv2 as cv


def validate_box(box, img_width, img_height):
	"""
	Validar que las dimensiones de un rectángulo no estén fuera de las dimensiones de una imagen.
	:param x1: límite izquierdo del rectángulo.
	:param y1: límite superior del rectángulo.
	:param x2: límite derecho del rectángulo.
	:param y2: límite inferior del rectángulo.
	:param img_width: ancho de la imagen.
	:param img_height: alto de la imagen.
	:return: True si el rectángulo es válido, False en caso contrario.
	"""
	x1, y1, x2, y2 = box
	if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
		return False
	if x1 > img_width or y1 > img_height or x2 > img_width or y2 > img_height:
		return False
	return True


def validate_boxes(boxes, img_width, img_height):
	"""
	De una lista de rectángulos, filtra los que son válidos, es decir, los que sus dimensiones no se salen de las dimensiones
	de la imagen.
	:param boxes: lista de rectángulos.
	:param img_width: ancho de la imagen.
	:param img_height: alto de la imagen.
	:return: lista filtrada.
	"""
	return [box for box in boxes if validate_box(box, img_width, img_height)]


def get_boxes(detections):
	return [box for box, _ in detections]


def get_confidences(detections):
	return [confidence for _, confidence in detections]


def filter_confidence(detections, threshold):
	return [(box, confidence) for box, confidence in detections if confidence >= threshold]


def filter_valid_dets(detections, img_width, img_height):
	return [(box, confidence) for box, confidence in detections if validate_box(box, img_width, img_height)]


def filter_valid_boxes(boxes, img_width, img_height):
	"""
	De una lista de rectángulos, filtra los que son válidos, es decir, los que sus dimensiones no se salen de las dimensiones
	de la imagen.
	:param boxes: lista de rectángulos.
	:param img_width: ancho de la imagen.
	:param img_height: alto de la imagen.
	:return: lista filtrada.
	"""
	return [box for box in boxes if validate_box(box, img_width, img_height)]


def intersection_over_union(A, B):
	(x1a, y1a, x2a, y2a) = A
	(x1b, y1b, x2b, y2b) = B
	# determine the (x, y)-coordinates of the intersection rectangle
	x1I = max(x1a, x1b)
	y1I = max(y1a, y1b)
	x2I = min(x2a, x2b)
	y2I = min(y2a, y2b)

	# compute the area of intersection rectangle
	interArea = max(0, x2I - x1I) * max(0, y2I - y1I)

	# compute the area of both the prediction and ground-truth rectangles
	boxAArea = (x2a - x1a) * (y2a - y1a)
	boxBArea = (x2b - x1b) * (y2b - y1b)

	iou = interArea / float(boxAArea + boxBArea - interArea)
	return iou


def non_max_suppression(boxes, overlap_thresh=0.3, iou_thresh=0.65):
	if len(boxes) == 0:
		return []
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	pick = []
	y2 = boxes[:, 3]
	idxs = np.argsort(y2)
	while len(idxs) > 0:
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)

		iou_overlap = np.array([intersection_over_union(boxes[i], b) for b in boxes[idxs[:last]]])
		idxs = np.delete(idxs, np.concatenate(([last], np.where(iou_overlap > iou_thresh)[0])))
	return pick


def box_area(box):
	x1, y1, x2, y2 = box
	return (x2 - x1) * (y2 - y1)


def box_center(box):
	x1, y1, x2, y2 = box
	return (x2 - x1) // 2, (y2 - y1) // 2


def fabiolas_adjust_box(img, face):
	"""
	Función de Fabiola para ajustar rectángulos de rostros.
	:param img:
	:param face:
	:return:
	"""
	image_rows, image_cols = img.shape[:2]
	x1, y1, x2, y2 = face
	face_width = x2 - x1
	face_height = y2 - y1
	face_center = (x1 + face_width / 2, y1 + face_height / 2)
	dif_w = dif_h = (face_height - face_width) / 2

	half_w = (face_width + dif_w) / 2
	if face_center[0] < half_w or face_center[0] + half_w > image_cols:
		half_w = min(face_center[0], image_cols - face_center[0])
	new_x = face_center[0] - half_w

	half_h = (face_height - dif_h) / 2
	new_y = face_center[1] - half_h

	return int(new_x), int(new_y), int(new_x + 2 * half_w), int(new_y + 2 * half_h)


def crop(img, box):
	x1, y1, x2, y2 = box
	return img[y1:y2, x1:x2]


def crop_with_margin(img, face, margin=0.4):
	"""
	Recortar imagen dando un margen extra.
	:author Fabiola
	:param img: image to crop
	:param face: face rect
	:param margin: margin around face to crop image
	:return: tuple(output cropped img, coordinates of cropped rect in img, coordinates of cropped rect in output)
	"""
	img_h, img_w, d = img.shape

	x1, y1, x2, y2 = face
	w = x2 - x1
	h = y2 - y1
	x_margin = int(w * margin)
	y_margin = int(h * margin)

	# --add margin--
	ini_x = x1 - x_margin
	end_x = x2 + x_margin
	ini_y = y1 - y_margin
	end_y = y2 + y_margin

	output = np.zeros((end_y - ini_y, end_x - ini_x, d), dtype=img.dtype)

	# --ensure that margin doesn't go beyond image size--
	x = max(ini_x, 0)
	brx = min(end_x, img_w)
	y = max(ini_y, 0)
	bry = min(end_y, img_h)

	# --coordinates of the cropped rect region in img--
	crop = x, y, brx, bry

	# --coordinates of the cropped rect region in output image--
	new_x = x - ini_x
	new_brx = new_x + brx - x
	new_y = y - ini_y
	new_bry = new_y + bry - y
	padding_crop = new_x, new_y, new_brx, new_bry

	# --cropping--
	output[new_y:new_bry, new_x:new_brx, :] = img[y:bry, x:brx, :]

	# --if margin goes beyond the size of the image, repeat last row/column of pixels--
	if new_y > 0:
		cv.repeat(output[new_y:new_y + 1, 0:output.shape[1]], new_y, 1, output[0:new_y, 0:output.shape[1]])

	if new_bry < output.shape[0]:
		cv.repeat(output[new_bry - 1: new_bry, 0:output.shape[1]], output.shape[0] - new_bry, 1, output[new_bry:output.shape[0], 0:output.shape[1]])

	if new_x > 0:
		cv.repeat(output[0:output.shape[0], new_x:new_x + 1], 1, new_x, output[0:output.shape[0], 0:new_x])

	if new_brx < output.shape[1]:
		cv.repeat(output[0:output.shape[0], new_brx - 1: new_brx], 1, output.shape[1] - new_brx, output[0:output.shape[0], new_brx:output.shape[1]])

	return output, crop, padding_crop
