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
import datetime

begin = time.perf_counter()

# Update Financial Data
grabFinance.grabFinance()

auth = redditInstance.initiate_instance()

print("CONNECTING TO DB", flush=True)


# print("COMPLETED", flush=True)


def runCountFinder(File):
    try:
        tic = time.perf_counter()
        cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
        myCursor = cnx.cursor()



        # Populate Portion  ************
        dataDF = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % File,
                             names=["Timestamp", "Subreddit", "Post/Comment"], lineterminator='\n')
        data = ''.join(map(str, dataDF['Post/Comment']))

        # # # Daily Portion **********
        # dataDF1 = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % fileName[0], names=["Timestamp", "Subreddit", "Post/Comment"], lineterminator='\n')
        # dataDF2 = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % fileName[1], names=["Timestamp", "Subreddit", "Post/Comment"], lineterminator='\n')
        #
        # # Concatenates all posts/comments into one string.
        # data1 = ''.join(map(str, dataDF1['Post/Comment']))
        # data2 = ''.join(map(str, dataDF2['Post/Comment']))
        # data = data1 + data2


        # NLTK (Alex Script) Returns Counts for Tickers in Ticker List
        result = findCounts.process_bodies(data)
        result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)
        result = findCounts.count_tickers(result, findCounts.tickers)
        resultDF = pd.DataFrame(list(result.items()), columns=['Ticker', 'Count'])

        # Calculates count of Tickers that returned values
        tickerList = resultDF['Ticker'].tolist()
        countList = resultDF['Count'].tolist()
        row_count = len(tickerList)

        # populate portion
        dateFix = File.split("_", 1)[1]
        dateFix = dateFix.split(".", 1)[0]
        dateFix = dateFix + " 00:00:00"
        endDate = datetime.datetime.strptime(dateFix,"%m-%d-%Y %H:%M:%S")
        dateFix = datetime.datetime.strptime(dateFix,"%m-%d-%Y %H:%M:%S")

        # daily portion
        # endDate = datetime.datetime.today()
        # dateFix = endDate - datetime.timedelta(days=1)


        # Iterates through count and updates mentions in database
        for i in range(0, row_count):
            try:
                newCount = countList[i]

                sql = "Update Trawler SET mentions = %s WHERE date = %s AND stock = %s"
                val = (newCount, dateFix, tickerList[i])
                myCursor.execute(sql, val)
                cnx.commit()
                # print("ROW UPDATED # %d" % i)
            except Exception as e:
                print("Error: ", e, " Info: ", dateFix, " ", tickerList[i])
                continue

        cnx.close
        toc = time.perf_counter()
        print("%s Completed***** in %0.4f seconds" % (File, (toc - tic)), flush=True)


    except Exception as e:

        print("ERROR: ", File, " :",e)








# CSV PORTION #################
directory = r'/home/dtujo/myoptane/Trawler/Dataframes'
fileList = []

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        fileList.append(filename)

with Parallel(n_jobs=-1) as parallel:
    print(parallel([delayed(runCountFinder)(file) for file in fileList]), flush=True)
# #################################################################

# daily portion #######################
# postDFList = grabPosts.post_and_timestamps(auth)
# postDF = postDFList[0]
# runCountFinder(postDF, postDFList[1])

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()
sql = "UPDATE Trawler SET mentions = 0 WHERE date > '2021-03-12 00:00:00' AND mentions IS NULL"
myCursor.execute(sql)
cnx.commit()
cnx.close

end = time.perf_counter()

print("Total time ran: %0.4f seconds" % (end - begin))