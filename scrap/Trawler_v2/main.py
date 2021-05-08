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

# grabFinance.grabFinance()

auth = redditInstance.initiate_instance()

# postDF = grabPosts.post_and_timestamps(auth)
# fileName = input("Enter file name: ")


print("CONNECTING TO DB", flush=True)


# print("COMPLETED", flush=True)


def runCountFinder(File):
    try:
        tic = time.perf_counter()
        cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
        myCursor = cnx.cursor()

        print("Reading CSV ", File )
        dataDF = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % File)


        # print("Concatenating data ", File)
        data = ''.join(map(str, dataDF['Post/Comment']))


        # print("RUNNING FIND COUNTS ", File, flush=True)
        result = findCounts.process_bodies(data)

        result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)

        result = findCounts.count_tickers(result, findCounts.tickers)

        # print("COMPLETED", flush=True)

        # print("TRANSFERRING TICKER COUNTS TO DATAFRAME", File, flush=True)
        resultDF = pd.DataFrame(list(result.items()), columns=['Ticker', 'Count'])

        # print("COMPLETED", flush=True)

        # resultDF.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\testing.csv', index=False)



        # print("SAVING VALUES TO LISTS ", File, flush=True)
        tickerList = resultDF['Ticker'].tolist()
        countList = resultDF['Count'].tolist()

        row_count = len(tickerList)
        # dateList = dataDF['Timestamp'].tolist()
        #
        #
        # dateFix = dateList[1]
        #
        # print(dateFix, " ", File)

        dateFix = File.split("_", 1)[1]
        dateFix = dateFix.split(".", 1)[0]
        dateFix = dateFix + " 00:00:00"
        dateFix = datetime.strptime(dateFix, "%m-%d-%Y %H:%M:%S")


        # if len(str(dateList[1])) == 10:
        #     dateFix = datetime.strptime(dateList[1], "%m/%d/%Y")
        # else:
        #     date_slice = dateList[1]
        #     date_slice = date_slice[0:10]
        #     dateFix = datetime.strptime(date_slice, "%Y-%m-%d")
        # print(" dateFix COMPLETED ", dateFix, flush=True)

        for i in range(0, row_count):
            sql1 = "SELECT mentions FROM Trawler WHERE date = %s AND stock = %s"
            val1 = (dateFix, tickerList[i])
            myCursor.execute(sql1, val1)
            dbMentionCount = myCursor.fetchone()
            # print(tickerList[i])
            # print(dbMentionCount)

            try:
                # print("count(%d) + dbcount(%d)" % (countList[i], dbMentionCount[0]))
                newCount = countList[i] + dbMentionCount[0]
            except Exception:
                print("Failed to add counts ", File)
                continue
            sql = "Update Trawler SET mentions = %s WHERE date = %s AND stock = %s"
            val = (newCount, dateFix, tickerList[i])
            myCursor.execute(sql, val)
            cnx.commit()
            # print("ROW UPDATED # %d" % i)

        cnx.close()
        toc = time.perf_counter()
        print("%s Completed***** in %0.4f seconds" % (File, (toc - tic)), flush=True)
    except Exception as e:
        print()
        print(File, " :",e)


# CSV PORTION #################
directory = r'/home/dtujo/myoptane/Trawler/Dataframes'
fileList = []
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        fileList.append(filename)

with Parallel(n_jobs=-1) as parallel:
    print(parallel([delayed(runCountFinder)(file) for file in fileList]), flush=True)
#################################################################

# daily portion #######################
# runCountFinder(postDF)
end = time.perf_counter()

print("Total time ran: %0.4f seconds" % (end - begin))