import time
from time import sleep
from joblib import Parallel, delayed
import pandas as pd
import mysql.connector

cnx = mysql.connector.connect(user='dtujo', password='dtujo-mys', host='localhost', database='DataSAIL')

myCursor = cnx.cursor()

recentDate = myCursor.execute("SELECT date FROM testingTrawler ORDER BY date DESC LIMIT  1")

print(recentDate)



