import numpy as np  #not using numpy in init, but numpy initi is easier (just google it)
import pandas as pd
import yfinance as yf
import datetime as dt
from scipy import stats

def Ticker(start_date, end_date, tickerSymbol):

    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    sCloses = tickerDf['Close'].to_list()
    sDates = tickerDf.index.to_list()
    sDates = pd.to_datetime(sDates)
    sDates = sDates.strftime("%Y-%m-%d")

    return sDates, sCloses

def Soaring(sDates, sCloses):

    # Algorithm:

    # Use Exponential Moving Averages (EMA) to smooth out the stock price over a window of 3 days
    # (as stock prices fluctuate too much between consecutive days)
    # Then calculate rate-of-change between EMAs
    # Calculate the slope of rate-of-change by comparing it with a 45 degree positive slope line
    # A stock is GOOD if it has a decent slope compared to that line
    # Even a flat rate-of-change is really good (slope of 0)
    # So most slopes end up in -ve values, because as price increases, slope falls

    # create timeseries with closing stock prices and their dates
    psCloses = pd.Series(sCloses, sDates)

    # panda has Exponential Weight Moving Average (aka EMA or EWMA or EWM)
    # EMA is like Simple Moving Average (SMA) over "Span" number of days except it is weight by how old it is
    # SMA Example. March 1st - $10, 2nd - $20, 3rd - 30. SMA = $20 for date March 3rd. March 1st SMA: NaN, 2nd: NaN
    # Next SMA:  March 2nd = #20, 3rd = #30, 4th = $40.  SMA = $30 for date March 4th.
    # SMA has values for all dates except the first 2 dates when Span = 3.
    # EMA is SMA multiplied by a fraction determined how old it is (the older SMAs become smaller)
    pMeans = psCloses.ewm(span=3, adjust=False).mean()

    # Perform Rate-of-change for consecutive EWMs
    # For example: pct_change for March 4th EWM ($23)  from March 3rd EWM ($20) => 15% change
    pChanges = pMeans.pct_change()

    # calculate slope using np.polyfit
    x = np.asarray(sDates)
    y = np.asarray(pChanges.values)
    x = x[1:]
    y = y[1:]

    # print ("x is")
    # print(x)
    # print("y is")
    # print(y)

    # # Create a sequance of integers from 0 to x.size to use in np.polyfit() call
    x_seq = np.arange(x.size) #

    # call numpy polyfit() method with x_seq, y
    # Find how rate_of_change compares against linear (or 45 degree slope)
    fit = np.polyfit(x_seq, y, 1)
    fit_fn = np.poly1d(fit)
    slope = fit[0]
    print("Slope is ", slope)

    # slope is so small and negative, this eq gets the value between 0 and 10
    soar =  100*slope + 5  # biased to 5 to move it to positive

    if (soar > 10):
        soar = 10
    elif (soar < 0):
        soar = 0

    # print('Slope = ', fit[0], ", ","Intercept = ", fit[1])
    # print(fit_fn)
    # print("PSCLOSES:")
    # print(psCloses)
    # print("PMEANS:")
    # print(pMeans)
    # print("PMEANS PCT CHANGE:")
    # print(pChanges)
    return soar



