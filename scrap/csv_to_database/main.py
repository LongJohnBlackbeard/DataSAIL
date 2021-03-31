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
<<<<<<< HEAD
        for column in data:
            date = data[column].values
        print(date)
=======
        for i in range(0, len(data.column[1])):
            print(i)
>>>>>>> 63f8a9598bd6a9a9dd984a9449aa7c0856f3d212

        # myCursor.execute()
    else:
        continue
