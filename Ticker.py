import yfinance as yf
import pandas as pd

debug = 0

def Ticker(start_date, end_date, tickerSymbol):
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    sCloses = tickerDf['Close'].to_list()
    sDates = tickerDf.index.to_list()
    sDates = pd.to_datetime(sDates)
    sDates = sDates.strftime("%Y-%m-%d")
    if debug == 1:
        print("sDates and sCloses")
        print(sDates, sCloses)
    return sDates, sCloses

