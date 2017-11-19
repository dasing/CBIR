import numpy as np
import cv2
from PARAMETER import *

def buildFilters():
	filters = []
	ksize = 31
	orientation = 4
	scale = 4
	bandWidth = 4
	for theta in np.arange(0, np.pi, np.pi/orientation):
		for sigma in np.arange(1, scale+1, 1 ):
			for lamda in np.arange(0, np.pi, np.pi/bandWidth):
				params = {'ksize':(ksize, ksize), 'sigma':sigma, 'theta':theta, 'lambd':lamda, 'gamma':0.02, 'psi':0, 'ktype': cv2.CV_32F}
				kern = cv2.getGaborKernel(**params)
				kern /= 1.5*kern.sum()
				filters.append(kern)
	return filters	

def buildRandomMatrix( featureDim ):

	reducedDim = int(round(featureDim * PROJECT_RATIO))
	size = reducedDim * featureDim

	genMatrix = np.random.normal( 0, 0.1, size ).reshape((reducedDim, featureDim))

	# print("reducedDim is {}".format(reducedDim))
	# print("size is {}".format(size))
	# print(genMatrix)

	return genMatrix


