import yfinance as yf
import pandas as pd
from urllib.request import Request, urlopen

def yahooRequest(tickerSymbol, tag):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (tickerSymbol, tag)
    request = Request(url)
    response = urlopen(request)
    content = response.read().decode().strip().strip('"')
    return content

def validTicker(tickerSymbol):
    tickerSymbol = tickerSymbol.upper()
    content = yahooRequest(tickerSymbol, 'n')
    if content != 'N/A':
        return True
    else:
        return False

def Ticker(start_date, end_date, tickerSymbol):
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    sCloses = tickerDf['Close'].to_list()
    sDates = tickerDf.index.to_list()
    sDates = pd.to_datetime(sDates)
    sDates = sDates.strftime("%Y-%m-%d")
    #print("sDates and sCloses")
    #print(sDates, sCloses)
    return sDates, sCloses

