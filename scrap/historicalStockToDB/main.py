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
import pymysql

connection = pymysql.connect(user='dtujo', password='dtujo-mys', host='localhost', db='DataSAIL')
cursor = connection.cursor()

tickers = pd.read_csv('tickertable.csv')
ts = timeseries.TimeSeries(key='DEO17X8J2DIV6483', output_format='pandas')
# ts = TimeSeries(key='DEO17X8J2DIV6483', output_format='pandas')

arr = tickers['Tickers'].to_numpy()
counter = 0

for ticker in arr:

    time.sleep(.6)

    daily_data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')

    daily_data = daily_data.reset_index()
    # print(daily_data)

    start_date = datetime(2021, 4, 12)
    # print(daily_data.date.iat[-1])

    dateRange = pd.date_range(start=daily_data.date.iat[-1], end=start_date, freq='D')[::-1]
    # print(dateRange)

    dateRangeDF = pd.DataFrame(index=dateRange)
    dateRangeDF.reset_index(inplace=True)
    print(dateRangeDF)
    temp_list = ['date']
    dateRangeDF.columns = temp_list

    dailyDataFinal = daily_data.merge(dateRangeDF, how='outer', on='date')

    print(dailyDataFinal)
    dailyDataFinal.to_csv('test.csv')

    for i, row in dailyDataFinal.iterrows():
        sql = "INSERT INTO `Trawler` (date, open, high, low, close, volume, stock) VALUES (" + "%s," * (len(row) - 1) + "%s, 'A')"
        cursor.execute(sql, tuple(row))

        connection.commit()

connection.close()
