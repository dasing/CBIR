from PARAMETER import *
from IMAGE import *
import os
import cPickle
import time

def constructSampleImgs(scope, featureType, filters, reducedMatrix):

	'''
		scope: global or local
		featureType: color or gabor filter

		this function is to compute features and return with list of samples with features
	'''

	sampleImgs = []
	## construct sampleImgs
	for i in range(len(TOPIC)):
		folder = DATAPATH + TOPIC[i]
		for filename in os.listdir(folder):
			if filename.endswith(".jpg"):
				# startTime = time.time()
				sample = Image(filename, i, scope, featureType, filters, reducedMatrix)
				sampleImgs.append(sample)
				# print("finish {}, time: {}".format(filename, time.time()-startTime))

	return sampleImgs


def restoreFeature( input, filters, reducedMatrix, debug = True):

	'''
		input: feature Input
		filters: constructed gabor filter
		reducedMatrix: contructed reducedMatrix

		this function is to get all sample feature, if cache ( ex: color), restore from file, else compute and save
		after get per-feature, if have multiple features, than concate all features to one final features
	'''

	perFeatureSamples = []
	for i in range(len(input)):
		print("here")
		scope = input[i][0]
		featureType = input[i][1]
		weight = input[i][2]

		featureFileName = ""

		if featureType == "COLOR":

			if scope == "GLOBAL":
				featureFileName = "GLOBAL_COLOR_HIST_" + str(n_bin)
			else:
				featureFileName = "LOCAL_COLOR_HIST_" +  str(n_bin) + "_" + str(n_slice)

			if RANDOM_PROJECTION:
				featureFileName += "_withRandomProjection_" + str(PROJECT_RATIO)

			print(featureFileName)
			
			#cache
			try:
				samples = cPickle.load(open(FEATURE_DATA_PATH + featureFileName, 'rb'))
				if debug:
					print 'load feature %s' % featureFileName
			except:
				if debug:
					print("compute feature {}".format(featureFileName))

				samples = constructSampleImgs(scope, featureType, filters, reducedMatrix)
				with open(FEATURE_DATA_PATH + featureFileName, 'wb') as f:
					cPickle.dump(samples, f)

		elif featureType == "GABOR_FILTER":
			print("compute gabor filter feature")
			samples = constructSampleImgs(scope, featureType, filters, reducedMatrix)


		for sample in samples:
			sample.hist *= weight 

		perFeatureSamples.append(samples)


	if len(input) == 1:
		return samples
	elif len(input) == 2:
		for m,n in zip(perFeatureSamples[0], perFeatureSamples[1]):
			m.hist = np.concatenate((m.hist, n.hist))
	elif len(input) == 3:
		for m,n,k in zip(perFeatureSamples[0], perFeatureSamples[1], perFeatureSamples[2]):
			m.hist = np.concatenate((m.hist, n.hist, k.hist))
	elif len(input) == 4:
		for m,n,k,l in zip(perFeatureSamples[0], perFeatureSamples[1], perFeatureSamples[2], perFeatureSamples[3]):
			m.hist = np.concatenate((m.hist, n.hist, k.hist, l.hist))

	return perFeatureSamples[0]

