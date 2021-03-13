import requests
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import datetime as dt
import numpy as np

tickers = pd.read_csv('tickertable.csv')
ts = TimeSeries(key='09150caf98mshdbd66c92f94bae1p1d9a46jsn48251394fdde', output_format="pandas")

arr = tickers['Tickers'].to_numpy()


counter = 0
for tick in arr:
    counter +=1
    daily_data, meta_data = ts.get_daily(symbol=tick, outputsize='full')
    daily_data.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\Stock Data\%s.csv' % tick)
    arr = np.delete(arr, np.where(arr == tick))
    time.sleep(12)
    if counter == 450:
        break

tickers_remaining = pd.DataFrame({'Tickers': arr})
tickers_remaining.to_csv(r'D:\Git\lewisuDataSAIL\scrap\finance_test\tickertable.csv')














