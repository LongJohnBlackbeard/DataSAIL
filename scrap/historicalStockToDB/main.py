import requests
import alpha_vantage
from alpha_vantage.alpha_vantage import timeseries
from alpha_vantage.timeseries import TimeSeries

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

daily_data, meta_data = ts.get_daily(symbol="A", outputsize='full')

cols = "`open`,`high`,`low`,`close`,`volume`"
print(cols)

for i, row in daily_data.iterrows():
    sql = "INSERT INTO `Trawler` (`" + cols + "`, stock) VALUES (" + "%s," * (len(row) - 1) + "%s, 'A')"
    cursor.execute(sql, tuple(row))

    connection.commit()

connection.close()
