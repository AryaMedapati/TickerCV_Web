from flask import render_template
from flask import request
from flask import Flask

import matplotlib
matplotlib.use("Agg")
#import numpy as np
import sqlite3
import pandas as pd
import datetime
import Ticker
import CV_Stats
import Plot
import Correlation
import HeatMap
import Soaring
import SQL_Database as sqd

app = Flask(__name__)

#Creating and Initializing DB before ticker is entered
db = sqd.startDB()
cursor = sqd.createDB(db)



class BestT:
    ticker = 'INTC'
    score = 3.5

bSoar = BestT()
bCorr = BestT()
@app.route('/')


def index():

    end_date = str(datetime.date.today())
    start_date1 = pd.to_datetime(end_date)
    start_date = start_date1 - datetime.timedelta(days=30)
    tdate = str(start_date.strftime("%Y-%m-%d"))
    #startDate = str(datetime.date.today())
    #endDate = (startDate.strftime("%Y-%m-%d"))

    query = 'tickersymbol'
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
    filename = url
    df = pd.read_csv(filename, lineterminator='\n')
    tdate = start_date

    defaultTS = 'SPY'
    inputTS = defaultTS

    # Ticker Symbol Entered
    if query in request.args:
        inputTS = request.args[query].upper()
    else:
        inputTS = defaultTS

    tickerSymbol = inputTS
    sDates, sCloses = Ticker.Ticker(start_date, end_date, tickerSymbol)

    # Check if Ticker is Valid and if not use default tickersymbol
    validTicker = True
    if len(sDates) < 1:
        validTicker = False
        tickerSymbol = defaultTS
        sDates, sCloses = Ticker.Ticker(start_date, end_date, tickerSymbol)

    scDates, tCases, scCloses = CV_Stats.CV_Stats(tdate, sDates, sCloses, df, end_date)
    sDates = scDates
    sCloses = scCloses
    sDates1 = pd.to_datetime(sDates)
    sDates1 = sDates1.strftime("%m-%d")
    score = Correlation.Correlate(sCloses, tCases)
    #sqd.updateDB(db, tickerSymbol, score,
    plot_url = Plot.Plot(sDates1, sCloses, tickerSymbol, tCases)
    cmap2 = matplotlib.cm.bone
    plot_url1 = HeatMap.HeatMap(score, tickerSymbol, cmap2, bCorr.score, bCorr.ticker)

    cmap = matplotlib.cm.plasma
    score1 = Soaring.Soaring(sDates, sCloses)
    plot_url2 = HeatMap.HeatMap(score1, tickerSymbol, cmap, bSoar.score, bSoar.ticker)


    return render_template('index.html', title=('%s vs COVID-19' % tickerSymbol),
        validTicker=validTicker, plot_url1=plot_url1, plot_url2=plot_url2, plot_url=plot_url, symbol=inputTS)
