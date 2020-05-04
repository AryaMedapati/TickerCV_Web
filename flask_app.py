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
import SQL_Password as sqp
import sqlite3

app = Flask(__name__)

#Creating and Initializing DB before ticker is entered
path = '/home/aryam/mysite/tickercv.db'
db = sqlite3.connect(path)
cursor = sqd.createDB(db)
defaultTS = 'SPY'
defaultDate = datetime.date.today()-datetime.timedelta(days=30)
sqd.updateDB(db, defaultTS, 1, 2, defaultDate)
corrrow = sqd.getMaxDBCorr(cursor)
rsirow = sqd.getMaxDBrsi(cursor)
db.close()

#Creating DB for Feedback
fpath = '/home/aryam/mysite/feedback.db'
fdb = sqlite3.connect(fpath)
fdbcursor = sqf.createFbDb(fdb)
fdb.close()

ppath = '/home/aryam/mysite/password.db'
pdb = sqlite3.connect(ppath)
pcursor = sqp.createPDB(pdb)
onerow = sqp.getRow0PDB(pcursor)
db.close()
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
    print("request")
    print(request)

    end_date = str(datetime.date.today()-datetime.timedelta(days=1))
    start_date1 = pd.to_datetime(end_date)
    start_date = start_date1 - datetime.timedelta(days=80)
    tdate = str(start_date.strftime("%Y-%m-%d"))

    db = sqlite3.connect(path)
    cursor = db.cursor()

    if debug == 1:
        print("All_rows")
        all_rows = sqd.getAllDB(cursor)
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

    if debug == 1:
        print("RSIrow")
        print(rsirow)
    sqd.updateDB(db, tickerSymbol, score, score1, end_date)

    plot_url = Plot.Plot(sDates1, sCloses, tickerSymbol, tCases)
    cmap2 = matplotlib.cm.spring
    plot_url1 = HeatMap.HeatMap(score, tickerSymbol, cmap2, corrrow[1], corrrow[0], -100, 100)

    cmap = matplotlib.cm.GnBu
    plot_url2 = HeatMap.HeatMap(score1, tickerSymbol, cmap, rsirow[2], rsirow[0], 0, 100)

    db.close()
    return render_template('index.html', title=('%s vs COVID-19' % tickerSymbol), validTicker=validTicker, plot_url1=plot_url1, plot_url2=plot_url2, plot_url=plot_url, symbol=inputTS, trending=trending)

@app.route('/about')
def about():
    return render_template('about.html', title=('Arya Medapati - About Page'))

@app.route('/detail')
def detail():
    db = sqlite3.connect(path)
    cursor = db.cursor()

    topcorrrows = sqd.getTopCorr(cursor)
    toprsirows = sqd.getToprsi(cursor)

    db.close()
    return render_template('detail.html', topcorrrows=topcorrrows, toprsirows=toprsirows)


@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    fdb = sqlite3.connect(fpath)
    fdbcursor = fdb.cursor()

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
    fdb.close()
    return render_template('feedback.html', all_rows=all_rows)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if debug == 1:
        print("request")
        print(request)

    if request.method == 'POST':
        passkey = request.form.get('lkey')
        num = request.form.get('num')
        deltick = request.form.get('deltick')
        if passkey == onerow[0]:
            db = sqlite3.connect(path)
            fdb = sqlite3.connect(fpath)

            cursor = db.cursor()
            fdbcursor = fdb.cursor()

            #comment = sqf.getAllFbDb(fdbcursor)

            sqf.deleteFb(fdb, num)
            sqd.deleteDB(db, deltick)

            clean = sqd.getAllDB(cursor)
            comment = sqf.getAllFbDb(fdbcursor)

            db.close()
            fdb.close()
            return render_template('cleanup.html', clean=clean, comment=comment, passkey=passkey)

    return render_template('login.html')






