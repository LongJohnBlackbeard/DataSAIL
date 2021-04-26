import csv
import os
import time

from joblib import Parallel, delayed

import findCounts
import grabPosts
import redditInstance
import pandas as pd
import mysql.connector
import grabFinance
from datetime import datetime
import joblib

begin = time.perf_counter()

grabFinance.grabFinance()

auth = redditInstance.initiate_instance()

postDF = grabPosts.post_and_timestamps(auth, grabPosts.reddit_input_lists)
# fileName = input("Enter file name: ")
directory = r'/home/dtujo/myoptane/Trawler/Dataframes'

print("CONNECTING TO DB", flush=True)


# print("COMPLETED", flush=True)


def runCountFinder(dataDF):
    tic = time.perf_counter()
    cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
    myCursor = cnx.cursor()

    # print("READING CSV FILE: %s" % file, flush=True)
    # dataDF = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % file)
    # print("COMPLETED", flush=True)

    # print("CONCATENATING POSTS AND COMMENTS", flush=True)
    data = ''.join(map(str, dataDF['Post/Comment']))
    # print("COMPLETED", flush=True)

    # print("RUNNING FIND COUNTS", flush=True)
    result = findCounts.process_bodies(data)

    result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)

    result = findCounts.count_tickers(result, findCounts.tickers)

    # print("COMPLETED", flush=True)

    # print("TRANSFERRING TICKER COUNTS TO DATAFRAME", flush=True)
    resultDF = pd.DataFrame(list(result.items()), columns=['Ticker', 'Count'])
    print("todays file ", "\n", resultDF, )
    # print("COMPLETED", flush=True)

    # resultDF.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\testing.csv', index=False)

    row_count = len(resultDF.index)

    # print("SAVING VALUES TO LISTS", flush=True)
    tickerList = resultDF['Ticker'].tolist()
    countList = resultDF['Count'].tolist()
    dateList = dataDF['Timestamp'].tolist()
    print(dateList[1])

    dateFix = dateList[1]

    # if len(str(dateList[1])) == 10:
    #     dateFix = datetime.strptime(dateList[1], "%m/%d/%Y")
    # else:
    #     date_slice = dateList[1]
    #     date_slice = date_slice[0:10]
    #     dateFix = datetime.strptime(date_slice, "%Y-%m-%d")
    # print("COMPLETED", flush=True)

    for i in range(0, row_count):
        sql1 = "SELECT mentions FROM testingTrawler WHERE date = %s AND stock = %s"
        val1 = (dateFix, tickerList[i])
        myCursor.execute(sql1, val1)
        dbMentionCount = myCursor.fetchone()
        # print(tickerList[i])
        # print(dbMentionCount)

        try:
            # print("count(%d) + dbcount(%d)" % (countList[i], dbMentionCount[0]))
            newCount = countList[i] + dbMentionCount[0]
        except Exception:
            continue
        sql = "Update testingTrawler SET mentions = %s WHERE date = %s AND stock = %s"
        val = (newCount, dateFix, tickerList[i])
        myCursor.execute(sql, val)
        cnx.commit()
        # print("ROW UPDATED # %d" % i)

    cnx.close()
    toc = time.perf_counter()
    print("%s Completed***** in %0.4f seconds" % ("Yesterdays data", (toc - tic)), flush=True)


# CSV PORTION #################
# fileList = []
# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):
#         fileList.append(filename)

# with Parallel(n_jobs=-1) as parallel:
#     print(parallel([delayed(runCountFinder)(i) for i in fileList]))
# #################################################################

# daily portion #######################
runCountFinder(postDF)
end = time.perf_counter()

print("Total time ran: %0.4f seconds" % (end - begin))