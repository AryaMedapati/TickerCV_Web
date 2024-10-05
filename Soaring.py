import random
import numpy as np  #not using numpy in init, but numpy initi is easier (just google it)
import math


def Soaring(series1, series2):
    #score = Correlate(series1, series2)  # we do not need to send x-axis as long as both series1 and series2
    maxS1 = max(series1) 
    maxS2 = max(series2)
    series1Norm = series1/maxS1 
    series2Norm = series2/maxS2
    #soaring is looking for when series 1 is beating series 2
    # or ((series1 - series2)/series2)**2
    diffSeriesN = (series1Norm/series2Norm) - 1

    diffSeriesNorm = diffSeriesN/max(diffSeriesN)
   
    #print("diffSeriesNorm is ", diffSeriesNorm)
    sumDS = sum(diffSeriesNorm)
    #print("sumDS is ", sumDS)
    meanDS = sumDS/len(diffSeriesNorm)
    #
    meanDS = math.sqrt(meanDS**2)
    print("meanDS is ", meanDS)
    score = (meanDS)*10
    return score

# series1 = np.random.rand(20)
# series2 = np.random.rand(20)

# print("Series 1 is equal to ", series1)
# print("Series 2 is equal to ", series2)

# score = Soaring(series1, series2)
# print("score is ", score)