import os
import pandas as pd
import mysql.connector

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')
myCursor = cnx.cursor()

directory = r'/home/dtujo/myoptane/Trawler/Dataframes'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(filename)
        data = pd.read_csv(r'/home/dtujo/myoptane/Trawler/Dataframes/%s' % filename)
        for column in data:
            date = data[column].values
        print(date)

        # myCursor.execute()
    else:
        continue