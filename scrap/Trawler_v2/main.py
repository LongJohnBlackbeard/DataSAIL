import csv

import findCounts
import grabPosts
import redditInstance
import pandas as pd
import mysql.connector

# auth = redditInstance.initiate_instance()
#
# dataDF = grabPosts.post_and_timestamps(auth, grabPosts.reddit_input_lists)
dataDF = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/Stocks_03-13-2021.csv')

data = ''.join(dataDF['Post/Comment'])
print(data)

result = findCounts.process_bodies(data)

result = findCounts.filter_pos_tokens(result, findCounts.target_pos_tags)

result = findCounts.count_tickers(result, findCounts.tickers)

print(type(result))

print(result)
resultDF = pd.DataFrame(list(result.items()), columns=['Ticker', 'Count'])

print(resultDF)

# resultDF.to_csv(r'D:\Git\lewisuDataSAIL\Dataframes\testing.csv', index=False)

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()

row_count = len(resultDF.index)

tickerList = resultDF['Ticker'].tolist()
countList = resultDF['Count'].tolist()

for i in range(0, row_count):
    sql = "Update testingTrawler SET count = %s WHERE date = %s AND stock = %s"
    val = (countList[i], dataDF[1]['Timestamp'], tickerList[i])
    myCursor.execute(sql, val)
    cnx.commit()

cnx.close()
