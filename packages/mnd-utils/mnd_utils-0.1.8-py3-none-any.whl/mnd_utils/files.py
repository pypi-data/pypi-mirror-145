import os
from os import path


def create_dir_of_file(file):
	"""
	Crea el directorio de un archivo, si este no existe.
	:param file: fichero.
	:return:
	"""
	directory, _ = path.split(file)
	if not path.exists(directory):
		os.makedirs(directory)


def replace_in_all_files(old, new, extensions=None, root='datasets/'):
	files = list_files(root, validExts=extensions)
	for f in files:
		_, name = os.path.split(f)
		if old in name:
			nf = f.replace(old, new)
			os.rename(src=f, dst=nf)


image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def list_images(basePath, contains=None, recursive=True):
	# return the set of files that are valid
	return list_files(basePath, validExts=image_types, contains=contains, recursive=recursive)


def list_files(basePath, validExts=None, contains=None, recursive=True):
	# loop over the directory structure
	for (rootDir, dirNames, filenames) in os.walk(basePath):
		# loop over the filenames in the current directory
		for filename in filenames:
			# if the contains string is not none and the filename does not contain
			# the supplied string, then ignore the file
			if contains is not None and filename.find(contains) == -1:
				continue

			# determine the file extension of the current file
			ext = filename[filename.rfind("."):].lower()

			# check to see if the file is an image and should be processed
			if validExts is None or ext.endswith(validExts):
				# construct the path to the image and yield it
				imagePath = os.path.join(rootDir, filename)
				yield imagePath
		if not recursive:
			break
