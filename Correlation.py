import numpy as np
import math

debug = 0

def Correlate(sCloses, tCases):
    #print("Correlation Function: ", len(sCloses), len(tCases))
    series1 = np.asarray(sCloses)
    series2 = np.asarray(tCases)
    maxS1 = max(series1)
    maxS2 = max(series2)
    if debug == 1:
        print("maxS1 - for Ticker Stock prices")
        print(maxS1)
    series1Norm = series1/maxS1
    series2Norm = series2/maxS2
    if debug == 1:
        print("series1Norm - for Ticker Stock prices")
        print(series1Norm)
        print("series2Norm - for COVID")
        print(series2Norm)

#    diffSeriesN = (1 - series2Norm/series1Norm)**2
    # or ((series1 - series2)/series1)**2

#   diffSeriesNorm = diffSeriesN/max(diffSeriesN)

#    sumDS = sum(diffSeriesNorm)

#    meanDS = sumDS/len(diffSeriesNorm)

#    score = (1 - meanDS)*10
    corr1 = np.corrcoef(series1Norm, series2Norm)
    if debug == 1:
        print("corr1")
        print(corr1)

    score = 100*corr1[0,1]

    if debug == 1:
        print("score - for Ticker Stock prices")
        print(score)
    if math.isnan(score):
        score = 0
    if debug == 1:
        print("score - for Ticker Stock prices")
        print(score)

    #if (score < 0):
        #score = 0 - score

    return score