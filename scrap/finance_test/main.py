import requests
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import datetime as dt
import numpy as np
import sys

tickers = pd.read_csv('tickertable.csv')
ts = TimeSeries(key='48217ae124msh8fc7e2e9fea05c8p17aa28jsn0b9326a23cb7', output_format="pandas")

arr = tickers['Tickers'].to_numpy()
print(arr)

counter = 0
try:
    for tick in arr:
        counter += 1
        daily_data, meta_data = ts.get_daily(symbol=tick, outputsize='full')
        daily_data.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\Stock Data\%s.csv' % tick)
        arr = np.delete(arr, np.where(arr == tick))
        tickers_remaining = pd.DataFrame({'Tickers': arr})
        tickers_remaining.to_csv(r'D:\Git\lewisuDataSAIL\scrap\finance_test\tickertable.csv')
        time.sleep(12)
        if counter == 450:
            break
except:
    e = sys.exc_info()[0]
    print('ERROR: ', e)



