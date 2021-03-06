from datetime import datetime, timedelta
import time
import requests
import alpha_vantage
from alpha_vantage.alpha_vantage import timeseries
# from alpha_vantage.timeseries import TimeSeries

import pandas as pd
import time
import datetime as dt
import numpy as np
import sys
import mysql.connector

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()

nasdaq = pd.read_csv('nasdaqlistFinish.csv')
ts = timeseries.TimeSeries(key='DEO17X8J2DIV6483', output_format='pandas')
# ts = TimeSeries(key='DEO17X8J2DIV6483', output_format='pandas')

# semiArr = tickers['Ticker'].to_numpy()
# fullArr = fullTickers['Ticker'].to_numpy()
nasdaqtick = nasdaq['Ticker'].to_numpy()

arr = []

# for ticker in semiArr:
#     arr.append(ticker)
#
# for ticker in fullArr:
#     if ticker not in arr:
#         arr.append(ticker)

for ticker in nasdaqtick:
    if ticker not in arr:
        arr.append(ticker)

for ticker in arr:
    if ("." in ticker) or ("-" in ticker):
        arr.remove(ticker)
counter = 0

try:
    for ticker in arr:
        tic = time.perf_counter()
        print(ticker, flush=True)

        daily_data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')

        daily_data = daily_data.reset_index()
        # print(daily_data)

        start_date = datetime(2021, 4, 12)
        # print(daily_data.date.iat[-1])

        dateRange = pd.date_range(start=daily_data.date.iat[-1], end=start_date, freq='D')[::-1]
        # print(dateRange)

        dateRangeDF = pd.DataFrame(index=dateRange)
        dateRangeDF.reset_index(inplace=True)
        # print(dateRangeDF)
        temp_list = ['date']
        dateRangeDF.columns = temp_list

        dailyDataFinal = daily_data.merge(dateRangeDF, how='outer', on='date')

        # print(dailyDataFinal)
        dailyDataFinal.to_csv('test.csv')

        row_count = len(dailyDataFinal.index)

        for i in range(0, row_count):
            sql = "INSERT INTO Trawler (date, open, high, low, close, volume, stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            if pd.isnull(dailyDataFinal.loc[i]['5. volume']):
                values_list = [str(dailyDataFinal.loc[i]['date']), 0, 0, 0, 0, 0]
            else:
                values_list = [str(dailyDataFinal.loc[i]['date']), dailyDataFinal.loc[i]['1. open'],
                               dailyDataFinal.loc[i]['2. high'], dailyDataFinal.loc[i]['3. low'],
                               dailyDataFinal.loc[i]['4. close'], int(dailyDataFinal.loc[i]['5. volume'])]
            # print(values_list)

            if len(values_list) == 6:
                values_list.append(ticker)
                # print("Add Ticker Row: ", values_list)
                # print(tuple(values_list))
                myCursor.execute(sql, tuple(values_list))
            else:
                addedValues = [0, 0, 0, 0, 0, ticker]
                values_list.append(addedValues)
                # print("Null row: ", values_list)
                myCursor.execute(sql, tuple(values_list))

            cnx.commit()
        toc = time.perf_counter()
        print("%s finished in %0.4f seconds" % (ticker, (toc - tic)), flush=True)
except ValueError as inst:
    print("Exception Occured: ")
    print(type(inst))
    print(inst.args)
    print(inst)

cnx.close()
