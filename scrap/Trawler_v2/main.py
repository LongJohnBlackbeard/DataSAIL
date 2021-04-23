import csv
import os

import findCounts
import grabPosts
import redditInstance
import pandas as pd
import mysql.connector
from datetime import datetime

# auth = redditInstance.initiate_instance()
#
# dataDF = grabPosts.post_and_timestamps(auth, grabPosts.reddit_input_lists)
# fileName = input("Enter file name: ")
directory = r'/home/dtujo/myoptane/Trawler/Dataframes'

print("CONNECTING TO DB", flush=True)
cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()
# print("COMPLETED", flush=True)

for filename in os.listdir(directory):
    if filename == ("wallstreetbets_03-22-2021.csv"):

        print("READING CSV FILE: %s" % filename, flush=True)
        dataDF = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % filename)
        # print("COMPLETED", flush=True)

        print("CONCATENATING POSTS AND COMMENTS", flush=True)
        data = ''.join(str(dataDF['Post/Comment']))
        # print("COMPLETED", flush=True)

        print("RUNNING FIND COUNTS", flush=True)
        result = findCounts.process_bodies(data)

        result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)

        result = findCounts.count_tickers(result, findCounts.tickers)

        # print("COMPLETED", flush=True)

        print("TRANSFERRING TICKER COUNTS TO DATAFRAME", flush=True)
        resultDF = pd.DataFrame(list(result.items()), columns=['Ticker', 'Count'])
        # print("COMPLETED", flush=True)

        # resultDF.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\testing.csv', index=False)



        row_count = len(resultDF.index)

        print("SAVING VALUES TO LISTS", flush=True)
        tickerList = resultDF['Ticker'].tolist()
        countList = resultDF['Count'].tolist()
        dateList = dataDF['Timestamp'].tolist()

        if len(dateList[1]) == 10:
            dateFix = datetime.strptime(dateList[1], "%m/%d/%Y")
        else:
            date_slice = dateList[1]
            date_slice = date_slice[0:10]
            dateFix = datetime.strptime(date_slice, "%Y-%m-%d")
        # print("COMPLETED", flush=True)

        # for i in range(0, row_count):
        #     sql1 = "SELECT mentions FROM testingTrawler WHERE date = %s AND stock = %s"
        #     val1 = (dateFix, tickerList[i])
        #     myCursor.execute(sql1, val1)
        #     dbMentionCount = myCursor.fetchone()
        #     # print(tickerList[i])
        #     # print(dbMentionCount)
        #
        #     try:
        #         # print("count(%d) + dbcount(%d)" % (countList[i], dbMentionCount[0]))
        #         newCount = countList[i] + dbMentionCount[0]
        #     except Exception:
        #         continue
        #     sql = "Update testingTrawler SET mentions = %s WHERE date = %s AND stock = %s"
        #     val = (newCount, dateFix, tickerList[i])
        #     myCursor.execute(sql, val)
        #     cnx.commit()
        #     # print("ROW UPDATED # %d" % i)
        #
        # print("%s Completed*****" % filename, flush=True)

cnx.close()
