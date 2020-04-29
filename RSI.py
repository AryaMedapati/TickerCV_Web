import pandas as pd
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

def Ticker(start_date, end_date, ticker):
    tickerData = yf.Ticker(ticker)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    sCloses = tickerDf['Close'].to_list()
    sDates = tickerDf.index.to_list()
    sDates = pd.to_datetime(sDates)
    sDates = sDates.strftime("%Y-%m-%d")

    return sDates, sCloses

# Get just the adjusted close
def computeRSI (sCloses, sDates, time_window, speriod):
    debug = 0
    if debug == 1:
        print("sCloses, sDates, time_window, speriod")
        print(sCloses)
        print(sDates)
        print(time_window)
        print(speriod)

    data = pd.Series(sCloses, sDates)
    diff = data.diff(1).dropna()        # diff in one field(one day)
    if debug == 1:
        print("data, diff")
        print(data)
        print(diff)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()

    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    rsi_sma = rsi.rolling(window=speriod).mean()
    rsiValues = rsi_sma.values
    rsi_trend = rsiValues[len(rsiValues)-1]
    if debug == 1:
        print("Rsi_trend")
        print(rsi_trend)
    return rsi_trend