import numpy as np


def Correlate(sCloses, tCases):
    #print("Correlation Function: ", len(sCloses), len(tCases))
    series1 = np.asarray(sCloses)
    series2 = np.asarray(tCases)
    maxS1 = max(series1)
    maxS2 = max(series2)
    series1Norm = series1/maxS1
    series2Norm = series2/maxS2

#    diffSeriesN = (1 - series2Norm/series1Norm)**2
    # or ((series1 - series2)/series1)**2

#   diffSeriesNorm = diffSeriesN/max(diffSeriesN)

#    sumDS = sum(diffSeriesNorm)

#    meanDS = sumDS/len(diffSeriesNorm)

#    score = (1 - meanDS)*10
    corr1 = np.corrcoef(series1Norm, series2Norm)
    score = 100*corr1[0,1]

    #if (score < 0):
        #score = 0 - score

    return score
