from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from api.vintedSaver import *
import numpy as np
import cv2
import sys
import time
import csv

def get_max_index(l):
	m = 0
	for i in range(len(l)):
		if l[i] > l[m]:
			m = i

	return m

def open_resize(file):
	t = time.time()
	image = cv2.imread(file)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	t = time.time()
	fac = 16
	down = (image.shape[1] // fac, image.shape[0] // fac)
	image = cv2.resize(image, down, interpolation= cv2.INTER_LINEAR)

	# reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	return image

def most_used_colors(image):
	# cluster the pixel intensities
	t = time.time()
	clt = KMeans(n_clusters = 3, n_init = 10)
	clt.fit(image)

	# Get the most used color
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	m = get_max_index(hist)

	return clt.cluster_centers_[m]

def rgb_to_string(color):
	names = []
	colors = []
	saver = Saver()

	for row in saver.loadColors():
		col = row.hex
		if len(col) == 0 or row.id in ['13', '14']:
			continue

		d = [int(col[i * 2:(i + 1) * 2], base=16) for i in range(3)]

		names.append(row.title)
		colors.append(d)

	kdt = KDTree(colors)
	d,i = kdt.query([int(x) for x in color])

	return names[i]

def getcolor(path):
	image = open_resize(path)
	color = most_used_colors(image)

	return color, rgb_to_string(color)
