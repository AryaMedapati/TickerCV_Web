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
    score = 10*corr1[0,1]

    if (score < 0):
        score = 0 - score

    if score < 2.4:
        gbw = "bad"
    if score > 2.4 and score < 3.0:
        gbw = "mediocre"
    if score > 3.0 and score < 3.65:
        gbw = "good"
    if score > 3.65:
        gbw = "excellent"

    return score