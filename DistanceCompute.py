import math
import numpy as np
from PARAMETER import *

class DistResult:
	def __init__(self, idx, filename, dist, topic):
		self.filename = filename
		self.idx = idx
		self.dist = dist
		self.topic = topic


def computeD1(hist_sample, hist_query, reducedMatrix):

	# print("hist_shape is {}".format(hist_sample.shape))
	# print(hist_sample)
	# print(hist_query)

	# if RANDOM_PROJECTION:
	# 	hist_sample = np.dot(reducedMatrix, hist_sample)
	# 	hist_query = np.dot(reducedMatrix, hist_query)

	# return 1.0 - np.sum(np.minimum(hist_sample, hist_query))
	return np.sum(np.absolute(hist_sample-hist_query))

def computeD2(hist_sample, hist_query):

	# print(np.dot(hist_sample, hist_sample))
	# print(np.dot(hist_sample, hist_query))
	return 2 - 2*np.dot(hist_sample, hist_query)