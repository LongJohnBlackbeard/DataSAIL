import time
from time import sleep
from joblib import Parallel, delayed
import pandas as pd
import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')

myCursor = cnx.cursor()

myCursor.execute("SELECT date FROM testingTrawler ORDER BY date DESC LIMIT  1")
records = myCursor.fetchall()
dateTuple = records[1]

# dateString = datetime.strftime(records[0], "%Y-%m-%d")
# print(type(dateString))
# print(dateString)

myCursor.close()



