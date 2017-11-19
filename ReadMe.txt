1. Change database path, DAPA_PATH, in PARAMETER.py, line1
2. Change INPUT feature, in hw1.py, line47, format: [ SCOPE, FEATURE, WEIGHT ] 
	SCOPE: type(string), "GLOBAL", "LOCAL"
	FEATURE: type(string), "COLOR", "GABOR_FILTER"
	WEIGHT: type(float), range: 0~1, sum of all feature weight should be 1
