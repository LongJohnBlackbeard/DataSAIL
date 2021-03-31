import os
import pandas as pd
import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()

directory = r'/home/dtujo/myoptane/Trawler/Dataframes'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(filename)
        data = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % filename)

        dates = data['Timestamp'].tolist()
        subreddit = data['Subreddit'].tolist()
        content = data['Post/Comment'].tolist()

        for i in range(0, len(dates)):
            date_time_obj = datetime.strptime(dates[i], "%d/%m/%Y")
            print()


        # myCursor.execute()
    else:
        continue
