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
import RSI
import SQL_Database as sqd
import SQL_Feedback as sqf

app = Flask(__name__)

#Creating and Initializing DB before ticker is entered
db = sqd.startDB('/home/aryam/mysite/tickercv.db')
cursor = sqd.createDB(db)
defaultTS = 'SPY'
defaultDate = datetime.date.today()-datetime.timedelta(days=30)
sqd.updateDB(db, defaultTS, 1, 2, defaultDate)

#Creating DB for Feedback
fdb = sqf.startFbDb('/home/aryam/mysite/feedback.db')
fdbcursor = sqf.createFbDb(fdb)

debug = 0


def latestScores(start_date, end_date, tickerSymbol):

    if debug == 1:
        print("start_date, end_Date, tickersymbol")
        print(start_date)
        print(end_date)
        print(tickerSymbol)

    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
    filename = url
    df = pd.read_csv(filename, lineterminator='\n')
    tdate = start_date

    sDates, sCloses = Ticker.Ticker(start_date, end_date, tickerSymbol)

    # Check if Ticker is Valid and if not use default tickersymbol
    validTicker = True
    if len(sDates) < 1:
        validTicker = False
        sDates, sCloses = Ticker.Ticker(start_date, end_date, defaultTS)


    scDates, tCases, scCloses = CV_Stats.CV_Stats(tdate, sDates, sCloses, df, end_date)
    sDates = scDates
    sCloses = scCloses
    sDates1 = pd.to_datetime(sDates)
    sDates1 = sDates1.strftime("%m-%d")
    score = Correlation.Correlate(sCloses, tCases)

    if debug == 1:
        print("sDates")
        print(sDates)

    score1 = RSI.computeRSI(sCloses, sDates, 10, 30)
    return score, score1, validTicker, sDates1, sCloses, tCases

@app.route('/')

def index():
    end_date = str(datetime.date.today())
    start_date1 = pd.to_datetime(end_date)
    start_date = start_date1 - datetime.timedelta(days=70)
    tdate = str(start_date.strftime("%Y-%m-%d"))

    all_rows = sqd.getAllDB(cursor)
    if debug == 1:
        print("All_rows")
        print(all_rows)

    row0 = sqd.getRow0DB(cursor)
    if debug == 1:
        print(row0)

    if row0[3] < end_date:
        all_rows = sqd.getAllDB(cursor)
        for row in all_rows:
            score, score1, validTicker, sDates1, sCloses, tCases = latestScores(start_date, end_date, row[0])
            sqd.updateDB(db, row[0], score, score1, end_date)

    query = 'tickersymbol'

      # Ticker Symbol Entered
    if query in request.args:
        inputTS = request.args[query].upper()
    else:
        inputTS = defaultTS

    tickerSymbol = inputTS
    score, score1, validTicker, sDates1, sCloses, tCases = latestScores(tdate, end_date, tickerSymbol)
    if score1 > 50:
        trending = True;
    else:
        trending = False;

    if validTicker == False:
        tickerSymbol = defaultTS

    corrrow = sqd.getMaxDBCorr(cursor)
    rsirow = sqd.getMaxDBrsi(cursor)

    if debug == 1:
        print("RSIrow")
        print(rsirow)
    sqd.updateDB(db, tickerSymbol, score, score1, end_date)

    plot_url = Plot.Plot(sDates1, sCloses, tickerSymbol, tCases)
    cmap2 = matplotlib.cm.spring
    plot_url1 = HeatMap.HeatMap(score, tickerSymbol, cmap2, corrrow[1], corrrow[0], -100, 100)

    cmap = matplotlib.cm.GnBu
    plot_url2 = HeatMap.HeatMap(score1, tickerSymbol, cmap, rsirow[2], rsirow[0], 0, 100)


    return render_template('index.html', title=('%s vs COVID-19' % tickerSymbol), validTicker=validTicker, plot_url1=plot_url1, plot_url2=plot_url2, plot_url=plot_url, symbol=inputTS, trending=trending)

@app.route('/about')
def about():
    return render_template('about.html', title=('Arya Medapati - About Page'))

@app.route('/detail')
def detail():
    topcorrrows = sqd.getTopCorr(cursor)
    toprsirows = sqd.getToprsi(cursor)
    return render_template('detail.html', topcorrrows=topcorrrows, toprsirows=toprsirows)


@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():

    uname = request.form.get('name1')
    ucomment = request.form.get('comment1')
    udate = datetime.date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        if (uname) and (ucomment):
            sqf.updateFbDb(fdb, uname, ucomment, udate)
            all_rows = sqf.getRecentFbDb(fdbcursor, 10)
            uname = ""
            ucomment = ""
            return render_template('showfb.html', all_rows=all_rows)

    all_rows = sqf.getRecentFbDb(fdbcursor, 10)
    return render_template('feedback.html', all_rows=all_rows)

@app.route('/cleanup')
def clean():
    clean = sqd.getAllDB(cursor)
    #comment = sqf.getAllFbDb(fdbcursor)
    query = 'num'
    if debug == 1:
        print("request.args")
        print(request.args)
    if query in request.args:
        inputID = request.args[query]
        sqf.deleteFb(fdb, inputID)
    else:
        inputID = 0
    if debug == 1:
        print("inputID")
        print(inputID)
    comment = sqf.getAllFbDb(fdbcursor)
    return render_template('cleanup.html', clean=clean, comment=comment, inputID=inputID)




