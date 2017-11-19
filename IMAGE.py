from PARAMETER import *
import cv2
import numpy as np
import math
import os
import matplotlib.pyplot as plt

class Image:
	def __init__(self, filename, topic, scope, featureType, filters, reducedMatrix):

		self.filename = filename
		self.topic = topic
		
		
		folder = DATAPATH + TOPIC[topic]
		channel = 1
		
		## read image
		if featureType == "COLOR":
			img = cv2.imread(os.path.join(folder, self.filename))
			width, height, channel = img.shape
		elif featureType == "GABOR_FILTER":
			img = cv2.imread(os.path.join(folder, self.filename), cv2.CV_LOAD_IMAGE_GRAYSCALE )
			width, height = img.shape

		if img is not None:
			if scope == "GLOBAL":
				self.hist = self.computeGlobalHist(img, featureType, filters, reducedMatrix)
			else:
				self.hist = self.computeLocalHist(img, featureType, filters, reducedMatrix, width, height, channel)
		else:
			return None
		

	def computeGlobalHist(self, img, featureType, filters, reducedMatrix):
	
		if featureType == "COLOR":	
			globalHist = self.computeColorHist(img)
		elif featureType == "GABOR":
			globalHist = self.computeGaborFilterResponse(img, filters)

		if RANDOM_PROJECTION:
			assert(globalHist.size == reducedMatrix.shape[1])
			globalHist = np.dot(reducedMatrix, globalHist)

		##normalize
		globalHist /= np.sum(globalHist)

		return globalHist
		
	def computeLocalHist(self, img, featureType, filters, reducedMatrix, width, height, channel):

		localHists = np.zeros(0)
		if featureType == "COLOR":
			localHists = np.zeros( (n_slice, n_slice, n_bin**channel) )
		elif featureType == "GABOR_FILTER":
			localHists = np.zeros( (n_slice, n_slice, len(filters)) )

		w_idx = np.around(np.linspace(0, width, n_slice+1)).astype(int)
		h_idx = np.around(np.linspace(0, height, n_slice+1)).astype(int)

		for _w in xrange(len(w_idx)-1):
			for _h in xrange(len(h_idx)-1):
				_img = img[w_idx[_w]:w_idx[_w+1], h_idx[_h]:h_idx[_h+1]]

				if featureType == "COLOR":
					localHists[_w][_h] = self.computeColorHist(_img)
				elif featureType == "GABOR_FILTER":
					localHists[_w][_h] = self.computeGaborFilterResponse(_img, filters)

		localHists = localHists.flatten()
		
		if RANDOM_PROJECTION:
			assert(localHists.size == reducedMatrix.shape[1])
			localHists = np.dot(reducedMatrix, localHists)

		localHists /= sum(localHists)

		return localHists
		

	def computeColorHist(self, img):
		
		width, height, channel = img.shape
		hist = np.zeros(n_bin ** channel)
		for i in range(width):
			for j in range(height):
				histIdx = 0
				for k in range(channel):
					bin_idx = int(math.floor(img[i][j][k]/gap))
					histIdx += bin_idx * ( n_bin ** ((channel-1)-k) )
				hist[histIdx] += 1
		return hist

	def computeGaborFilterResponse(self, img, filters):
		
		response = np.zeros(len(filters))
		
		for idx, kern in enumerate(filters):
			fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
			threshold = np.mean(fimg)
			bw = (fimg > threshold)
			response[idx] = np.sum(bw)

			## show image
			# imgplot = plt.imshow(fimg, cmap="Greys_r" )
			# plt.show()
		return response
		
