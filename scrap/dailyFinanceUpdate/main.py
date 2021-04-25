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

myCursor.close()

startDate = dateObject
endDate = datetime.today()
dateRange = pd.date_range(start=startDate, end=endDate, freq="D")[::-1]

dateRangeDF = pd.DataFrame(index=dateRange)
dateRangeDF.reset_index(inplace=True)
temp_list = ['date']
dateRangeDF.columns = temp_list

print(dateRangeDF)
dateRangeList = dateRangeDF['date'].to_list()


def dataGrabSend(ticker):
    cnx1 = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
    myCursor1 = cnx1.cursor()

    daily_data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
    daily_data = daily_data.reset_index()

    dailyDataFinal = daily_data.merge(dateRangeDF, how='outer', on='date')

    for index, row in dailyDataFinal.iterrows():
        if row['date'] in dateRangeList:
            sql = "INSERT INTO testingTrawler1 (date, open, high, low, close, volume, stock) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            if pd.isnull(row['5. volume']):
                values_list = [row['date'], 0, 0, 0, 0, 0]
            else:
                values_list = [row['date'], row['1. open'], row['2. high'], row['3. low'], row['4. close'],
                               row['5. volume']]
            if len(values_list) == 6:
                values_list.append(ticker)
                # print("Add Ticker Row: ", values_list)
                # print(tuple(values_list))
                myCursor1.execute(sql, tuple(values_list))
            else:
                addedValues = [0, 0, 0, 0, 0, ticker]
                values_list.append(addedValues)
                # print("Null row: ", values_list)
                myCursor1.execute(sql, tuple(values_list))
            print(row['date'], " executed")

            cnx1.commit()
            cnx1.close()


dataGrabSend("GME")
