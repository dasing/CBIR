from PARAMETER import *
from DistanceCompute import *

def evaluation(results, topic):

	'''
		results: list of class DistResult
		topic: label
	'''

	precision = 0.0
	hit = 0.0
	count = 1.0
	AP = 0.0

	for result in results:
		if result.topic == topic:
			hit += 1
			precision = hit/count
			AP += precision
		else:
			precision = hit/count

		count += 1

	AP /= per_topic_gt

	return AP

def performanceAnalysis(samples, distType):

	print("In performance analysis")
	MAP = [ 0 for x in range(len(TOPIC)) ]

	## compute distance
	for idx, sample in enumerate(samples):
		# print("query {} sample {}".format(idx, sample.filename))
		results = []
		for idx, query in enumerate(samples):
			hist_sample = sample.hist
			hist_query = query.hist

			if distType == "D1":
				diff = computeD1(hist_sample, hist_query)
			elif distType == "D2":
				diff = computeD2(hist_sample, hist_query)

			result = DistResult(idx, query.filename, diff, query.topic)
			results.append(result)

		## sort result
		results.sort(key = lambda x: x.dist)

		# for result in results:
		# 	print(result.filename)
		# 	print(result.dist)
		# 	print(result.topic)

		AP = evaluation(results, sample.topic)
		MAP[sample.topic] += AP
		# print("AP: {}".format(AP))

	MAP[:] = [x/per_topic_gt for x in MAP]
	MMAP = sum(MAP) / len(TOPIC)

	return MAP, MMAP