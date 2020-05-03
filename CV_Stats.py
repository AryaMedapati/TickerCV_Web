import pandas as pd
import datetime

debug = 0

def CV_Stats(tdate, sDates, sCloses, df, end_date):
    cCases = {}
    tCases = []
    scDates = []
    scCloses = []
    while True:
        #print("tdate is ", tdate)
        #mask = (df['Date'] >= tdate) & (df['Date'] <= tdate)
        mask = (df['Date'] == tdate)
        #print("mask is ")
        #print(mask)
        df2 = df.loc[mask]
        #print("DF2 is")
        #print(df2)
        tconfirm = df2['Confirmed'].sum()
        #print("Date: ", tdate, "\tConfirmed cases: ", tconfirm)

        # tdate1 = pd.to_datetime(tdate)
        # tdate2 = tdate1.strftime("%m-%d")
        cCases.update( {str(tdate) : tconfirm} )
        if tdate == end_date:
            break
        tdate1 = pd.to_datetime(tdate)
        tdate1 = tdate1 + datetime.timedelta(days=1)
        tdate = tdate1.strftime("%Y-%m-%d")
        #print("Next date ", tdate)
    i=0
    for sd in sDates:
        if sd in cCases.keys():
            tCases.append(cCases[sd])
            scDates.append(sd)
            scCloses.append(sCloses[i])
        else:
            print("Can't find ", sd, " in ccases.")
        i += 1
    if debug == 1:
        print("Dates, Cases, Closes")
        print(scDates)
        print(tCases)
        print(scCloses)
    return scDates, tCases, scCloses