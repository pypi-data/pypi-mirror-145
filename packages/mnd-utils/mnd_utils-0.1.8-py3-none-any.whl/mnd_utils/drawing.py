import cv2 as cv


def draw_rects(img, color, boxes, scores=None):
	"""
	Dibuja un conjunto de rectángulos en la imagen con el color especificado. Opcionalmente los rectángulos pueden tener
	una puntuación.
	:param img: immagen.
	:param boxes: rectángulos.
	:param color: color.
	:param scores: puntuaciones [opcional].
	:return:
	"""
	draw = img.copy()
	for i in range(len(boxes)):
		box = boxes[i]
		cv.rectangle(draw, (box[0], box[1]), (box[2], box[3]), color, 2, 4)
		if scores:
			text = "{:.2f}".format(scores[i])
			cv.putText(draw, text, (box[0], box[1] - 5), cv.FONT_HERSHEY_SIMPLEX, 1.5, color, 2, cv.LINE_AA)
	return draw


def draw_face_metadata(img, color, box, age, gender, ethnicity):
	draw = img.copy()
	age = age or '-'
	gender = gender or '-'
	ethnicity = ethnicity or '-'
	data_str = str.join(' | ', (age, gender, ethnicity))
	cv.rectangle(draw, (box[0], box[1]), (box[2], box[3]), color, 2, 4)
	cv.putText(draw, data_str, (box[0], box[1] - 5), cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv.LINE_AA)
	return draw
