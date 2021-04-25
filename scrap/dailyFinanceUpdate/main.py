import time
from time import sleep
from joblib import Parallel, delayed
import pandas as pd
import mysql.connector
from datetime import datetime
from alpha_vantage.alpha_vantage import timeseries

ts = timeseries.TimeSeries(key='DEO17X8J2DIV6483', output_format='pandas')
nasdaq = pd.read_csv('nasdaqlist.csv')
nasdaqTick = nasdaq['Ticker'].to_numpy()
arr = []
for tick in nasdaqTick:
    if tick not in arr:
        arr.append(tick)

for tick in arr:
    if ("." in tick) or ("-" in tick):
        arr.remove(tick)

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()

myCursor.execute("SELECT date FROM testingTrawler ORDER BY date DESC LIMIT  1")
records = myCursor.fetchall()
dateTuple = records[0]
dateObject = dateTuple[0]
dateString = datetime.strftime(dateObject, "%Y-%m-%d")

print(type(dateString))
print(dateString)

myCursor.close()

startDate = dateObject
endDate = datetime.today()
dateRange = pd.date_range(start=endDate, end=startDate, freq="D")
print(dateRange)


def dataGrabSend(ticker):
    cnx1 = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
    myCursor1 = cnx1.cursor()

    daily_data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
