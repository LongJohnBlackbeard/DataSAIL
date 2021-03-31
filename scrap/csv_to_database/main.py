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
            print(len(dates[i]))
            print(i)
            if len(dates[i]) == 10:
                print(dates[i])
                date_time_obj = datetime.strptime(dates[i], "%m/%d/%Y")
                print(date_time_obj)
            else:
                date_string = dates[i]
                print(date_string)
                date_slice = date_string[0:11]
                print(date_slice)
                date_time_obj = datetime.strptime(date_slice, "%m/%d/%Y")
                print(date_time_obj)
    else:
        continue
