import concurrent.futures
import multiprocessing
from datetime import datetime
import time
import requests
from alpha_vantage.alpha_vantage import timeseries
from joblib import Parallel, delayed

# from alpha_vantage import timeseries
import pandas as pd
import mysql.connector
import multiprocessing as mp

import joblib
import sys
from time import sleep



# import list of tickers
nasdaq = pd.read_csv('nasdaqlist.csv')
# set alpha-vantage connection string
ts = timeseries.TimeSeries(key='DEO17X8J2DIV6483', output_format='pandas')
# Grab ticker and put into list
nasdaqTick = nasdaq['Ticker'].to_numpy()

arr = []
# Screens tickers for invalid characters

for tick in nasdaqTick:
    if tick not in arr:
        arr.append(tick)


for tick in arr:
    if ("." in tick) or ("-" in tick):
        arr.remove(tick)


def data_grab_send(ticker):
    
    try:
        # mysql connection
        cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
        myCursor = cnx.cursor()

        print("Starting %s" % ticker, flush=True)
        sleep(30)
        tic1 = time.perf_counter()
        # grabs data from alpha-vantage
        daily_data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
        # reset index of the pd
        daily_data = daily_data.reset_index()
        # creates a date range to grab data and fill in missing dates
        start_date = datetime(2021, 5, 15)
        dateRange = pd.date_range(start=daily_data.date.iat[-1], end=start_date, freq='D')[::-1]
        # sends daterange to pd and resets index
        dateRangeDF = pd.DataFrame(index=dateRange)
        dateRangeDF.reset_index(inplace=True)
        # adding new column
        temp_list = ['date']
        dateRangeDF.columns = temp_list
        # merging two df
        dailyDataFinal = daily_data.merge(dateRangeDF, how='outer', on='date')
        # creates a count of dates and saves to a variable
        row_count = len(dailyDataFinal.index)

        # Loop through every date and grabs data and sends to database
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
        toc1 = time.perf_counter()
        done = ("%s finished in %0.4f seconds" % (ticker, (toc1 - tic1)))
        print(done, flush=True)

        cnx.commit()
        cnx.close()
    except ValueError:
        print("For stock: ", ticker, " ", ValueError, flush=True)
        pass


    
    


# multi-threading
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     futures = []
#     for stock in arr:
#         futures.append((executor.submit(data_grab_send(stock))))
#     for future in concurrent.futures.as_completed(futures):
#         try:
#             print(future.result())
#         except Exception as exc:
#             print(exc)

# multi-processing
# pool = mp.Pool(25)
#
#
# if __name__ == "__main__":
#     print("There are %d CPU's on this machine" % multiprocessing.cpu_count())
# for stock in arr:
#     pool.apply_async(data_grab_send(stock))
#
# pool.close()
# pool.join()

# joblib

tic = time.perf_counter()

with Parallel(n_jobs=50) as parallel:
    print(parallel([delayed(data_grab_send)(i) for i in arr]), flush=True)

toc = time.perf_counter()
print("Total time: %0.4f" % (toc - tic))


# regular

# for i in arr:
#     data_grab_send(i)
#
# toc = time.perf_counter()
# print("finished in %0.4f seconds" % (toc - tic))

# cnx.close()
