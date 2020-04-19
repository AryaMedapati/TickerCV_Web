from flask import render_template
from flask import request
from flask import Flask

import matplotlib
matplotlib.use("Agg")
#import numpy as np
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
defaultTS = 'SPY'
defaultDate = datetime.date.today()-datetime.timedelta(days=70)
sqd.updateDB(db, defaultTS, 1, 2, defaultDate)

def latestScores(start_date, end_date, tickerSymbol):

    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
    filename = url
    df = pd.read_csv(filename, lineterminator='\n')
    tdate = start_date

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
    score1 = Soaring.Soaring(sDates, sCloses)
    return score, score1, validTicker, sDates1, sCloses, tCases

@app.route('/')

def index():
    end_date = str(datetime.date.today())
    start_date1 = pd.to_datetime(end_date)
    start_date = start_date1 - datetime.timedelta(days=30)
    tdate = str(start_date.strftime("%Y-%m-%d"))


    row0 = sqd.getRow0DB(cursor)
    print(row0)
    if row0[3] < end_date:
        all_rows = sqd.getAllDB(cursor)
        for row in all_rows:
            score, score1, validTicker, sDates1, sCloses, tCases = latestScores(row[3], end_date, row[0])
            sqd.updateDB(db, row[0], score, score1, end_date)

    query = 'tickersymbol'

      # Ticker Symbol Entered
    if query in request.args:
        inputTS = request.args[query].upper()
    else:
        inputTS = defaultTS

    tickerSymbol = inputTS
    score, score1, validTicker, sDates1, sCloses, tCases = latestScores(tdate, end_date, tickerSymbol)

    corrrow = sqd.getMaxDBCorr(cursor)
    soarrow = sqd.getMaxDBSoar(cursor)
    sqd.updateDB(db, tickerSymbol, score, score1, end_date)

    plot_url = Plot.Plot(sDates1, sCloses, tickerSymbol, tCases)
    cmap2 = matplotlib.cm.bone
    plot_url1 = HeatMap.HeatMap(score, tickerSymbol, cmap2, corrrow[1], corrrow[0])

    cmap = matplotlib.cm.plasma
    plot_url2 = HeatMap.HeatMap(score1, tickerSymbol, cmap, soarrow[2], soarrow[0])


    return render_template('index.html', title=('%s vs COVID-19' % tickerSymbol),
        validTicker=validTicker, plot_url1=plot_url1, plot_url2=plot_url2, plot_url=plot_url, symbol=inputTS)

#@app.route('/about')



@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():

    if request.method == 'POST':
        uname = request.form.get('name1')
        ucomment = request.form.get('comment1')
        return render_template('showfb.html', uname=uname, ucomment=ucomment)

    return render_template('feedback.html')




