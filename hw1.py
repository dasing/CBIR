from PARAMETER import *
import IMAGE
from LOAD_DATA import *
from DistanceCompute import *
from EVALUATION import *
from FILTER import *

def computeFeatureDim( input, gaborFilterSize ):
	'''
		input: feature input, lists of feature, order is ["SCOPE", "FEATURE", WEIGHT]
		gaboFilterSize: size of gabor filter

		this function is to compute total feature dimension.
	'''
	dim = 0
	for i in range(len(input)):
		s,f,w = input[i]
		if s == "GLOBAL":
			if f == "COLOR":
				dim += (n_bin ** 3)
			else:
				dim += gaborFilterSize
		else:
			if f == "COLOR":
				dim += (n_slice ** 2)*(n_bin ** 3)
			else:
				dim += (n_slice ** 2)*gaborFilterSize
	return dim

def getFeatureName(input):
	'''
		input: feature input, lists of feature, order is ["SCOPE", "FEATURE", WEIGHT]
		
		this function is to get final feature name
	'''
	featureName = ""
	for i in range(len(input)):
		s, w, f = input[i]
		featureName += s + "_" + w + "_" + str(f) + "_"
	
	print(featureName)
	return featureName

if __name__ == "__main__":

	
	input = [ ["LOCAL", "COLOR", 0.5], ["LOCAL", "GABOR_FILTER", 0.5] ]
	distType = "D1" ## D1, D2

	featureName = getFeatureName(input)
	filters = buildFilters() ## build gabor filter

	reducedMatrix = np.zeros(0)
	if RANDOM_PROJECTION:
		featureName +=  ("with_RANDOM_PROJECTION_" + str(PROJECT_RATIO) )
		featureDim = computeFeatureDim( input, len(filters))
		print("featureDim is {}".format(featureDim))
		reducedMatrix = buildRandomMatrix(featureDim)
		
	samples = restoreFeature(input, filters, reducedMatrix)
	MAP , MMAP = performanceAnalysis(samples, distType)

	# output result
	for i in xrange(len(TOPIC)):
		print("Category {}, MAP {}".format(TOPIC[i], MAP[i]))

	print("{}, {},MMAP is {}".format(featureName, distType, MMAP))
	